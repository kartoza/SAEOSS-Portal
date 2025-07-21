import logging
import pathlib
import typing

import dateutil.parser
import langcodes
import yaml
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model.license import LicenseNotSpecified
from ckanext.spatial.interfaces import ISpatialHarvester
from ..cli import _CkanSaeossDataset, _CkanResource
from ..constants import DATASET_Harvest_MINIMAL_SET_OF_FIELDS_MAPPING
import re
import ast
from ckanext.spatial.harvesters.csw import CSWHarvester
import xml.etree.ElementTree as ET
from flask import json

import six
from six.moves.urllib.parse import urlparse, urlunparse, urlencode
from ckan import model

from ckan.plugins.core import SingletonPlugin, implements

from ckanext.harvest.interfaces import IHarvester
from ckanext.harvest.model import HarvestObject
from ckanext.harvest.model import HarvestObjectExtra as HOExtra

from ckanext.spatial.lib.csw_client import CswService
from ckanext.spatial.harvesters.base import SpatialHarvester, text_traceback

logger = logging.getLogger(__name__)

class CSWHarvestingPlugin(SpatialHarvester, SingletonPlugin):
    """Custom plugin to deal with harvesting-related customizations.

    This class exists in order to work around a bug in ckanext-spatial:

        https://github.com/ckan/ckanext-spatial/issues/277

    The mentioned bug prevents being able to have a CKAN extension plugin using both
    the `IValidators` and the `ISpatialHarvester` interfaces at the same time.

    As an alternative, we have implemented the current plugin class with the aim
    to use it strictly for customization of the harvesters (_i.e._ implement the
    ISpatialHarvester interface) while the main plugin class
    (saeoss_plugin.SaeossPlugin) is still handling all of the other SAEOSS
    customizations.

    """

    plugins.implements(IHarvester)

    csw = None

    def info(self):
        return {
            'name': 'saeoss_harvesting',
            'title': 'SAEOSS CSW Harvester',
            'description': 'A server that implements OGC\'s Catalog Service for the Web (CSW) standard (TEST)'
            }

    def get_original_url(self, harvest_object_id):
        obj = model.Session.query(HarvestObject).\
                                    filter(HarvestObject.id==harvest_object_id).\
                                    first()

        parts = urlparse(obj.source.url)

        params = {
            'SERVICE': 'CSW',
            'VERSION': '2.0.2',
            'REQUEST': 'GetRecordById',
            'OUTPUTSCHEMA': 'http://www.isotc211.org/2005/gmd',
            'OUTPUTFORMAT':'application/xml' ,
            'ID': obj.guid
        }

        url = urlunparse((
            parts.scheme,
            parts.netloc,
            parts.path,
            None,
            urlencode(params),
            None
        ))

        return url

    def output_schema(self):
        return 'gmd'
    
    # def gather_stage(self, harvest_job):
    #     log = logging.getLogger(__name__ + '.CSW.gather')
    #     log.debug('CswHarvester gather_stage for job: %r', harvest_job)
    #     # Get source URL
    #     url = harvest_job.source.url

    #     self._set_source_config(harvest_job.source.config)

    #     try:
    #         self._setup_csw_client(url)
    #     except Exception as e:
    #         self._save_gather_error('Error contacting the CSW server: %s' % e, harvest_job)
    #         return None

    #     query = model.Session.query(HarvestObject.guid, HarvestObject.package_id).\
    #                                 filter(HarvestObject.current==True).\
    #                                 filter(HarvestObject.harvest_source_id==harvest_job.source.id)
    #     guid_to_package_id = {}

    #     for guid, package_id in query:
    #         guid_to_package_id[guid] = package_id

    #     guids_in_db = set(guid_to_package_id.keys())

    #     # extract cql filter if any
    #     cql = self.source_config.get('cql')

    #     log.debug('Starting gathering for %s' % url)
    #     guids_in_harvest = set()
    #     try:
    #         for identifier in self.csw.getidentifiers(page=10, outputschema=self.output_schema(), cql=cql):
    #             try:
    #                 log.info('Got identifier %s from the CSW', identifier)
    #                 if identifier is None:
    #                     log.error('CSW returned identifier %r, skipping...' % identifier)
    #                     continue

    #                 guids_in_harvest.add(identifier)
    #             except Exception as e:
    #                 self._save_gather_error('Error for the identifier %s [%r]' % (identifier,e), harvest_job)
    #                 continue

    #     except Exception as e:
    #         log.error('Exception: %s' % text_traceback())
    #         self._save_gather_error('Error gathering the identifiers from the CSW server [%s]' % six.text_type(e), harvest_job)
    #         return None

    #     new = guids_in_harvest - guids_in_db
    #     delete = guids_in_db - guids_in_harvest
    #     change = guids_in_db & guids_in_harvest

    #     ids = []
    #     for guid in new:
    #         obj = HarvestObject(guid=guid, job=harvest_job,
    #                             extras=[HOExtra(key='status', value='new')])
    #         obj.save()
    #         ids.append(obj.id)
    #     for guid in change:
    #         obj = HarvestObject(guid=guid, job=harvest_job,
    #                             package_id=guid_to_package_id[guid],
    #                             extras=[HOExtra(key='status', value='change')])
    #         obj.save()
    #         ids.append(obj.id)
    #     for guid in delete:
    #         obj = HarvestObject(guid=guid, job=harvest_job,
    #                             package_id=guid_to_package_id[guid],
    #                             extras=[HOExtra(key='status', value='delete')])
    #         model.Session.query(HarvestObject).\
    #               filter_by(guid=guid).\
    #               update({'current': False}, False)
    #         obj.save()
    #         ids.append(obj.id)

    #     if len(ids) == 0:
    #         self._save_gather_error('No records received from the CSW server', harvest_job)
    #         return None

    #     return ids

    # def fetch_stage(self,harvest_object):

        # Check harvest object status
        status = self._get_object_extra(harvest_object, 'status')

        if status == 'delete':
            # No need to fetch anything, just pass to the import stage
            return True

        log = logging.getLogger(__name__ + '.CSW.fetch')
        log.debug('CswHarvester fetch_stage for object: %s', harvest_object.id)

        url = harvest_object.source.url
        try:
            self._setup_csw_client(url)
        except Exception as e:
            self._save_object_error('Error contacting the CSW server: %s' % e,
                                    harvest_object)
            return False

        identifier = harvest_object.guid
        try:
            record = self.csw.getrecordbyid([identifier], outputschema=self.output_schema())
        except Exception as e:
            self._save_object_error('Error getting the CSW record with GUID %s' % identifier, harvest_object)
            return False

        if record is None:
            self._save_object_error('Empty record for GUID %s' % identifier,
                                    harvest_object)
            return False

        try:
            # Save the fetch contents in the HarvestObject
            # Contents come from csw_client already declared and encoded as utf-8
            # Remove original XML declaration
            content = re.sub('<\?xml(.*)\?>', '', record['xml'])

            harvest_object.content = content.strip()
            harvest_object.save()
        except Exception as e:
            self._save_object_error('Error saving the harvest object for GUID %s [%r]' % \
                                    (identifier, e), harvest_object)
            return False

        log.debug('XML content saved (len %s)', len(record['xml']))
        return True

    def gather_stage(self, harvest_job):
        log = logging.getLogger(__name__ + '.CSW.gather')
        log.debug('CswHarvester gather_stage for job: %r', harvest_job)

        url = harvest_job.source.url
        self._set_source_config(harvest_job.source.config)

        try:
            self._setup_csw_client(url)
        except Exception as e:
            self._save_gather_error(f'Error contacting the CSW server: {e}', harvest_job)
            return None

        # Build GUID-to-package_id map for existing objects
        query = model.Session.query(HarvestObject.guid, HarvestObject.package_id).\
            filter(HarvestObject.current == True).\
            filter(HarvestObject.harvest_source_id == harvest_job.source.id)
        guid_to_package_id = {guid: package_id for guid, package_id in query}
        guids_in_db = set(guid_to_package_id.keys())

        # Read optional settings from config
        cql = self.source_config.get('cql')
        max_records = self.source_config.get('max_records')

        try:
            max_records = int(max_records) if max_records else None
        except ValueError:
            log.warning(f"Invalid max_records value: {max_records}")
            max_records = None

        log.debug(f"Starting gathering for {url} with max_records={max_records}")
        guids_in_harvest = set()

        record_count = 0  # <- Track how many we've processed
        try:
            for identifier in self.csw.getidentifiers(
                page=10,
                outputschema=self.output_schema(),
                cql=cql
            ):
                if identifier is None:
                    log.error('CSW returned None identifier, skipping...')
                    continue

                guids_in_harvest.add(identifier)
                record_count += 1

                log.info('Got identifier %s from the CSW', identifier)

                # ENFORCE LIMIT HERE
                if max_records is not None and record_count >= max_records:
                    log.info(f"Reached max_records limit: {max_records}")
                    break

        except Exception as e:
            log.error('Exception during identifier retrieval: %s', text_traceback())
            self._save_gather_error(f'Error gathering the identifiers from the CSW server [{e}]', harvest_job)
            return None

        new = guids_in_harvest - guids_in_db
        delete = guids_in_db - guids_in_harvest
        change = guids_in_db & guids_in_harvest

        ids = []
        for guid in new:
            obj = HarvestObject(guid=guid, job=harvest_job,
                                extras=[HOExtra(key='status', value='new')])
            obj.save()
            ids.append(obj.id)

        for guid in change:
            obj = HarvestObject(guid=guid, job=harvest_job,
                                package_id=guid_to_package_id[guid],
                                extras=[HOExtra(key='status', value='change')])
            obj.save()
            ids.append(obj.id)

        for guid in delete:
            obj = HarvestObject(guid=guid, job=harvest_job,
                                package_id=guid_to_package_id[guid],
                                extras=[HOExtra(key='status', value='delete')])
            model.Session.query(HarvestObject).filter_by(guid=guid).update({'current': False}, False)
            obj.save()
            ids.append(obj.id)

        if not ids:
            self._save_gather_error('No records received from the CSW server', harvest_job)
            return None

        return ids

    def fetch_stage(self, harvest_object):
        status = self._get_object_extra(harvest_object, 'status')
        if status == 'delete':
            return True  # skip fetching for deletes

        log = logging.getLogger(__name__ + '.CSW.fetch')
        log.debug('CswHarvester fetch_stage for object: %s', harvest_object.id)

        url = harvest_object.source.url

        try:
            self._setup_csw_client(url)
        except Exception as e:
            self._save_object_error('Error contacting the CSW server: %s' % e, harvest_object)
            return False

        identifier = harvest_object.guid

        try:
            record = self.csw.getrecordbyid([identifier], outputschema=self.output_schema())
        except Exception as e:
            self._save_object_error('Error getting the CSW record with GUID %s' % identifier, harvest_object)
            return False

        if record is None:
            self._save_object_error('Empty record for GUID %s' % identifier, harvest_object)
            return False

        try:
            xml_content = record['xml']
            content = re.sub('<\?xml(.*)\?>', '', xml_content).strip()

            # -- Keyword filtering --
            config = harvest_object.source.config
            if config:
                try:
                    config_dict = json.loads(config)
                    keywords_filter = config_dict.get('keywords', [])
                except Exception as e:
                    self._save_object_error(f"Invalid config JSON: {e}", harvest_object)
                    return False

                if keywords_filter:
                    # Parse the XML and check for keywords
                    try:
                        root = ET.fromstring(xml_content)
                        namespaces = {'gmd': 'http://www.isotc211.org/2005/gmd'}
                        keyword_elements = root.findall(".//gmd:keyword/gco:CharacterString", {
                            'gmd': 'http://www.isotc211.org/2005/gmd',
                            'gco': 'http://www.isotc211.org/2005/gco'
                        })

                        found_keywords = []
                        for elem in keyword_elements:
                            if elem is not None and elem.text:
                                found_keywords += [kw.strip() for kw in elem.text.split(';') if kw.strip()]

                        # Check if any of the filter keywords are present
                        if not any(kw in found_keywords for kw in keywords_filter):
                            log.debug('Skipping record %s due to missing keywords. Found: %s', identifier, found_keywords)
                            return False
                    except Exception as e:
                        self._save_object_error(f"Error parsing XML for keywords: {e}", harvest_object)
                        return False
            # -- End keyword filtering --

            harvest_object.content = content
            harvest_object.save()
        except Exception as e:
            self._save_object_error(
                'Error saving the harvest object for GUID %s [%r]' % (identifier, e),
                harvest_object
            )
            return False

        log.debug('XML content saved (len %s)', len(record['xml']))
        return True

    def _setup_csw_client(self, url):
        self.csw = CswService(url)


