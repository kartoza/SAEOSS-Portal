# -*- coding: utf-8 -*-
"""
A blueprint rendering stac harvest page.
"""
import inspect
import uuid
from flask import Blueprint, request
from ckan.plugins import toolkit
import logging
from pystac_client import Client
from concurrent import futures
from dateutil.parser import parse as datetime_parse
from datetime import date, datetime
import datetime as dt
import json
from ckanext.harvest import utils as harvest_utils
from ..cli import utils
from ckan.common import c
from ckan import model

logger = logging.getLogger(__name__)


stac_blueprint = Blueprint(
    "stac_harvest", __name__, template_folder="templates", url_prefix="/stac_harvest"
)

def columns_to_dict(self):
    dict_ = {}
    for key in self.__mapper__.c.keys():
        dict_[key] = getattr(self, key)
    return dict_

@stac_blueprint.route("/create_job", methods = ['POST', 'GET'])
def create_job():
    """A blueprint rendering stac harvest template.

    """
    return toolkit.render("stac_harvest/create.html")

@stac_blueprint.route("/", methods = ['POST', 'GET'])
def view():
    """A blueprint rendering stac harvest template.

    """
    user = c.userobj.id
    logger.debug(f"user {c.userobj}")

    return toolkit.render("stac_harvest/view.html")

@stac_blueprint.route("/view_jobs/", methods = ['POST', 'GET'])
def view_jobs():
    """A blueprint rendering stac harvest template.

    """
    user = c.userobj.id
    q = f""" select * from stac_harvester """
    result = model.Session.execute(q)
    jobs = result.fetchall()

    context = []

    for job in jobs:
        context.append(dict(job))

    logger.debug(f"jobs data {context}")

    return json.dumps(context, sort_keys=True, default=str)

@stac_blueprint.route("/create/", methods = ['POST', 'GET'])
def create_stac():
    if request.method == 'POST':
        user = c.userobj.id
        data = request.get_json()
        for _data in data["value"]:
            url = _data["url"]
            number_records = _data["number_records"]
            owner_org = _data["owner_org"]

        catalog = Client.open(url)
        stac_collections = list(catalog.get_collections())

        try:
            max_count = int(number_records)
        except:
            max_count = 10
            logger.info("max_count is not an integer, setting it to 10")

        created = 0
        processed = 0

        stac_harvester_id = uuid.uuid4()
        user_id = c.userobj.fullname
        q = f""" insert into stac_harvester values('{stac_harvester_id}', '{user_id}', '{owner_org}', '{url}', '{number_records}', 'running', '', '{datetime.now()}') """
        model.Session.execute(q)
        model.Session.commit()
            

        for collection in stac_collections:
            collection_items = collection.get_items()

            for item in collection_items:
                if processed > max_count:
                    return
                logger.debug(f"collection_items {collection_items}")
                data_dict = {}
                meta_date = item.properties.get(
                    "start_datetime",
                    item.properties.get(
                        "datetime",
                        datetime.now().isoformat()
                    )
                )
                meta_date = datetime_parse(meta_date).strftime("%Y-%m-%dT%H:%M:%S")

                data_dict["id"] = catalog.id + item.id
                data_dict["title"] = f"{catalog.title} - {collection.title} - {item.properties.get('title', item.id)}"
                data_dict["name"] = item.id
                # there might or might not be notes, let's take the notes of the catalog for the moment
                data_dict["notes"] = collection.description
                data_dict["responsible_party-0-individual_name"] = "responsible individual name"
                data_dict["responsible_party-0-role"] = "owner"
                data_dict["responsible_party-0-position_name"] = "position name"
                data_dict["dataset_reference_date-0-reference"] = meta_date
                data_dict["dataset_reference_date-0-reference_date_type"] = "1"
                data_dict["topic_and_sasdi_theme-0-iso_topic_category"] = "farming"
                data_dict["owner_org"] = owner_org
                data_dict["lineage_statement"] = "lineage statement"
                data_dict["private"] = False
                data_dict["metadata_language_and_character_set-0-dataset_language"] = "en"
                data_dict["metadata_language_and_character_set-0-metadata_language"] = "en"
                data_dict["metadata_language_and_character_set-0-dataset_character_set"] = "utf-8"
                data_dict["metadata_language_and_character_set-0-metadata_character_set"] = "utf-8"
                data_dict["lineage"] = "lineage statement"
                data_dict["distribution_format-0-name"] = "distribution format"
                data_dict["distribution_format-0-version"] = "1.0"
                data_dict["spatial"] = json.dumps(item.geometry)
                data_dict["spatial_parameters-0-equivalent_scale"] = "equivalent scale"
                data_dict["spatial_parameters-0-spatial_representation_type"] = "001"
                data_dict["spatial_parameters-0-spatial_reference_system"] = "EPSG:3456"
                data_dict["metadata_date"] = meta_date
                data_dict["resources"] = []
                if data_dict.get('dataset_reference_date', None):
                    del data_dict['dataset_reference_date']
                logger.debug('stac_item:', str(data_dict))
                # TODO dataset thumbnail, tags,
                for link in item.links:
                    if link.rel == "thumbnail":
                        data_dict["resources"].append({
                            "name": link.target,
                            "url": link.target,
                            "format": "jpg",
                            "format_version":
                                "1.0"
                        })
                    if link.rel == "self":
                        data_dict["resources"].append({
                            "name": "STAC Item",
                            "url": link.target,
                            "format": "JSON",
                            "format_version":
                                "1.0"
                        })

                with futures.ThreadPoolExecutor(3) as executor:
                    logger.debug(f"harvest id {stac_harvester_id}")
                    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {'name': user})
                    future = executor.submit(utils.create_single_dataset, user, data_dict)
                    logger.debug(future.result())
                    if str(future.result()) != 'DatasetCreationResult.NOT_CREATED_ALREADY_EXISTS':
                        created += 1
                    processed += 1

                _q = f""" update stac_harvester set message = '{future.result()}', status = 'finished' WHERE harvester_id = '{stac_harvester_id}' """
                _result = model.Session.execute(_q)
                model.Session.commit()
                    
        return json.dumps({"message": "finished"})
    
    return json.dumps({"message": "empty request"})
