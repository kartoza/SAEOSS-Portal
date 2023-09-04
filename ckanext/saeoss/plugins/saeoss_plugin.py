import logging
import typing
from collections import OrderedDict
from functools import partial
import uuid

import ckan.plugins as plugins
import ckan.lib.helpers as h
import ckan.lib.search as search
import ckan.lib.plugins as lib_plugins
import ckan.plugins.toolkit as toolkit
from datetime import date, datetime
import datetime as dt
import dateutil.parser
from ckan import model
from ckan.common import _, g
from ckan.common import c
from flask import Blueprint
from sqlalchemy import orm
import yaml
from xmltodict3 import XmlTextToDict

from ckanext.harvest.utils import DATASET_TYPE_NAME as HARVEST_DATASET_TYPE_NAME
from ckanext.harvest.harvesters.ckanharvester import CKANHarvester
import logging

from ..logic.action import ckan_custom_actions

from ..model.reporting_tool import ReportingTool


from .. import (
    helpers,
)
from ..blueprints.saeoss import saeoss_blueprint
from ..blueprints.xml_parser import xml_parser_blueprint
from ..blueprints.map import map_blueprint
from ..blueprints.validator import validator_blueprint
from ..blueprints.saved_searches import saved_searches_blueprint
from ..blueprints.news import news_blueprint
from ..blueprints.contact import contact_blueprint
from ..blueprints.sys_stats import stats_blueprint
from ..cli import commands
from ..logic.action import ckan as ckan_actions
from ..logic.action import saeoss as saeoss_actions

from ..logic import (
    converters,
    validators,
)

from ..logic.auth import ckan as ckan_auth
from ..logic.auth import pages as ckanext_pages_auth
from ..logic.auth import saeoss as saeoss_auth
from ..model.user_extra_fields import UserExtraFields
import ckan.logic as logic
import json

import ckanext.saeoss.plugins.utils as utils
import ckan.lib.uploader as uploader
logger = logging.getLogger(__name__)
ValidationError = logic.ValidationError

class SaeossPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController)
    plugins.implements(plugins.IResourceController)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IPluginObserver)

    def group_form(self):
        pass

    def before_load(self, plugin_class):
        """IPluginObserver interface requires reimplementation of this method."""
        pass

    def after_load(self, service):
        """Control plugin loading mechanism

        This method is implemented by the SaeossPlugin because we are adding
        a 1:1 relationship between our `UserExtraFields` model and CKAN's `User` model.

        SQLAlchemy expects relationships to be configured on both sides, which means
        we have to modify CKAN's User model in order to make the relationship work. We
        do that in this function.

        """

        model.User.extra_fields = orm.relationship(
            UserExtraFields, back_populates="user", uselist=False
        )

    def before_unload(self, plugin_class):
        """IPluginObserver interface requires reimplementation of this method."""
        pass

    def after_unload(self, service):
        """IPluginObserver interface requires reimplementation of this method."""
        pass

    def after_create(self, context, pkg_dict):
        """IPackageController interface requires reimplementation of this method."""
        return context, pkg_dict

    def after_delete(self, context, pkg_dict):
        """IPackageController interface requires reimplementation of this method."""
        return context, pkg_dict

    def after_search(self, search_results, search_params):
        """IPackageController interface requires reimplementation of this method."""

        context = {}
        logger.debug(f"after search {context}")
        facets = OrderedDict()
        default_facet_titles = {
            "groups": _("Groups"),
            "tags": _("Tags"),
        }

        for facet in h.facets():
            if facet in default_facet_titles:
                facets[facet] = default_facet_titles[facet]
            else:
                facets[facet] = facet

        # Facet titles
        for plugin in plugins.PluginImplementations(plugins.IFacets):
            facets = plugin.dataset_facets(facets, "dataset")

        data_dict = {
            "fq": "",
            "facet.field": list(facets.keys()),
        }

        if not getattr(g, "user", None):
            data_dict["fq"] = "+capacity:public " + data_dict["fq"]

        query = search.query_for(model.Package)
        try:
            if context.get("ignore_auth") or c.userobj.sysadmin:
                labels = None
            else:
                labels = lib_plugins.get_permission_labels().get_user_dataset_labels(
                    c.userobj
                )

            query.run(data_dict, permission_labels=labels)
        except:
            query.run(data_dict, permission_labels=None)

        facets = query.facets

        # organizations in the current search's facets.
        group_names = []
        for field_name in ("groups", "organization"):
            group_names.extend(facets.get(field_name, {}).keys())

        groups = (
            model.Session.query(model.Group.name, model.Group.title)
            .filter(model.Group.name.in_(group_names))
            .all()
            if group_names
            else []
        )
        group_titles_by_name = dict(groups)
        restructured_facets = {}
        for key, value in facets.items():
            restructured_facets[key] = {"title": key, "items": []}
            for key_, value_ in value.items():
                new_facet_dict = {"name": key_}
                if key in ("groups", "organization"):
                    display_name = group_titles_by_name.get(key_, key_)
                    display_name = (
                        display_name if display_name and display_name.strip() else key_
                    )
                    new_facet_dict["display_name"] = display_name
                else:
                    new_facet_dict["display_name"] = key_
                new_facet_dict["count"] = value_
                restructured_facets[key]["items"].append(new_facet_dict)
        search_results["search_facets"] = restructured_facets

        return search_results

    def after_show(self, context, pkg_dict):
        """IPackageController interface requires reimplementation of this method."""
        return context, pkg_dict

    def after_update(self, context, pkg_dict):
        """IPackageController interface requires reimplementation of this method."""
        return context, pkg_dict

    def before_index(self, pkg_dict):
        """IPackageController interface requires reimplementation of this method."""
        return pkg_dict
    
    def before_show(self, resource_dict):
        u'''
        Extensions will receive the validated data dict before the resource
        is ready for display.

        Be aware that this method is not only called for UI display, but also
        in other methods, like when a resource is deleted, because package_show
        is used to get access to the resources in a dataset.
        '''
        return resource_dict
    
    def before_create(self, context, resource):
        u'''
        Extensions will receive this before a resource is created.

        :param context: The context object of the current request, this
            includes for example access to the ``model`` and the ``user``.
        :type context: dictionary
        :param resource: An object representing the resource to be added
            to the dataset (the one that is about to be created).
        :type resource: dictionary
        '''

        logger.debug(f"resource create {resource}")

    def before_update(self, mapper, connection, instance):
        u'''
        Receive an object instance before that instance is UPDATEed.
        '''

        logger.debug(f"resource update {instance}")

    def before_delete(self, mapper, connection, instance):
        u'''
        Receive an object instance before that instance is PURGEd.
        (whereas usually in ckan 'delete' means to change the state property to
        deleted, so use before_update for that case.)
        '''
        pass

    def before_search(self, search_params: typing.Dict):
        logger.debug(f"debug search {search_params.get('extras', {})}" )
        
        
        start_date = search_params.get("extras", {}).get("ext_start_reference_date")
        end_date = search_params.get("extras", {}).get("ext_end_reference_date")
        if start_date is not None or end_date is not None:
            parsed_start = _parse_date(start_date) if start_date else start_date
            parsed_end = _parse_date(end_date) if end_date else end_date
            temporal_query = (
                f"reference_date:[{parsed_start or '*'} TO {parsed_end or '*'}]"
            )
            filter_query = " ".join((search_params["fq"], temporal_query))
            search_params["fq"] = filter_query
        search_params["fq"] = utils.handle_search(search_params)

        reporter_search_id = uuid.uuid4()
        if c.userobj != None:
            user_id = c.userobj.id
            q = f""" insert into reporting_tool values('{reporter_search_id}', '{user_id}', '{json.dumps(search_params)}', '','{datetime.now()}') """
            result = model.Session.execute(q)
            model.Session.commit()
        
        return search_params

    def before_view(self, pkg_dict: typing.Dict):
        return pkg_dict

    def create(self, entity):
        """IPackageController interface requires reimplementation of this method."""
        return entity

    def edit(self, entity):
        """IPackageController interface requires reimplementation of this method."""
        return entity

    def delete(self, entity):
        """IPackageController interface requires reimplementation of this method."""
        return entity

    def read(self, entity):
        """IPackageController interface requires reimplementation of this method."""
        return entity

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "../templates")
        toolkit.add_public_directory(config_, "../public")
        toolkit.add_resource("../assets", "ckanext-saeoss")

    def get_commands(self):
        return [
            commands.saeoss,
            commands.shell,
        ]

    def get_auth_functions(self) -> typing.Dict[str, typing.Callable]:
        return {
            "package_publish": ckan_auth.authorize_package_publish,
            "package_update": ckan_auth.package_update,
            "package_patch": ckan_auth.package_patch,
            "ckanext_pages_update": ckanext_pages_auth.authorize_edit_page,
            "ckanext_pages_delete": ckanext_pages_auth.authorize_delete_page,
            "ckanext_pages_show": ckanext_pages_auth.authorize_show_page,
            "request_dataset_maintenance": (
                saeoss_auth.authorize_request_dataset_maintenance
            ),
        }

    def get_actions(self) -> typing.Dict[str, typing.Callable]:
        return {
            "package_create": ckan_actions.package_create,
            "package_update": ckan_actions.package_update,
            "package_patch": ckan_actions.package_patch,
            "package_show": ckan_actions.package_show,
            "saeoss_version": saeoss_actions.show_version,
            "user_patch": ckan_actions.user_patch,
            "user_update": ckan_actions.user_update,
            "user_create": ckan_actions.user_create,
            "user_show": ckan_actions.user_show,
            "resource_create": ckan_custom_actions.resource_create,
            "resource_update": ckan_custom_actions.resource_update,
        }

    def get_validators(self) -> typing.Dict[str, typing.Callable]:
        return {
            "value_or_true": validators.value_or_true_validator,
            "srs_validator": validators.srs_validator,
            "bbox_converter": converters.bbox_converter,
            "spatial_resolution_converter": converters.spatial_resolution_converter,
            "convert_choices_select_to_int": converters.convert_choices_select_to_int,
            "check_if_number": converters.check_if_number,
            "check_if_int": converters.check_if_int,
            "convert_select_custom_choice_to_extra": converters.convert_select_custom_choice_to_extra,
            "doi_validator": validators.doi_validator,
            "stac_validator": validators.stac_validator,
            "metadata_default_standard_name": converters.default_metadata_standard_name,
            "metadata_default_standard_version": converters.default_metadata_standard_version,
            "lineage_source_srs_validator": validators.lineage_source_srs_validator,
        }

    def is_fallback(self) -> bool:
        return False

    def package_types(self) -> typing.List:
        return []

    def get_helpers(self):
        return {
            "saeoss_default_spatial_search_extent": partial(
                helpers.get_default_spatial_search_extent, 0.001
            ),
            "build_nav_main": helpers.build_pages_nav_main,
            "default_bounding_box": helpers.get_default_bounding_box,
            "convert_geojson_to_bounding_box": helpers.convert_geojson_to_bbox,
            "extent_to_bbox": helpers.convert_string_extent_to_bbox,
            # "saeoss_themes": helpers.get_saeoss_themes,
            "iso_topic_categories": helpers.get_iso_topic_categories,
            "saeoss_show_version": helpers.helper_show_version,
            "user_is_org_member": helpers.user_is_org_member,
            "org_member_list": helpers.org_member_list,
            "user_is_staff_member": helpers.user_is_staff_member,
            "get_featured_datasets": helpers.get_featured_datasets,
            "get_recently_modified_datasets": helpers.get_recently_modified_datasets,
            "get_all_datasets_count": helpers.get_all_datasets_count,
            "saeoss_org_memberships": helpers.get_org_memberships,
            "mod_scheming_flatten_subfield": helpers.mod_scheming_flatten_subfield,
            "get_today_date": helpers.get_today_date,
            "get_maintenance_custom_other_field_data": helpers.get_maintenance_custom_other_field_data,
            "get_release": helpers.get_current_release,
            "get_saved_searches": helpers.get_saved_searches,
            "get_recent_news": helpers.get_recent_news,
            "get_featured_datasets_count": helpers.get_featured_datasets_count,
            "get_user_name": helpers.get_user_name,
            "get_user_name_from_url": helpers.get_user_name_from_url,
            "get_user_id": helpers.get_user_id,
            "get_seo_metatags": helpers.get_seo_metatags,
            "get_datasets_thumbnail": helpers.get_datasets_thumbnail,
            "get_year": helpers.get_year,
            "get_user_dashboard_packages": helpers.get_user_dashboard_packages,
            "get_org_public_records_count": helpers.get_org_public_records_count,
        }

    def get_blueprint(self) -> typing.List[Blueprint]:
        return [
            saeoss_blueprint,
            xml_parser_blueprint,
            map_blueprint,
            validator_blueprint,
            saved_searches_blueprint,
            news_blueprint,
            contact_blueprint,
            stats_blueprint,
        ]

    def dataset_facets(
        self, facets_dict: typing.OrderedDict, package_type: str
    ) -> typing.OrderedDict:
        if package_type != HARVEST_DATASET_TYPE_NAME:
            # facets_dict["reference_date"] = toolkit._("Reference Date")
            facets_dict["harvest_source_title"] = toolkit._("Harvest source")
            facets_dict["featured"] = toolkit._("Featured Metadata records")
        return facets_dict

    def group_facets(
        self, facets_dict: typing.OrderedDict, group_type: str, package_type: str
    ) -> typing.OrderedDict:
        """IFacets interface requires reimplementation of all facets-related methods

        In this case we do not really need to override this method, but need to satisfy
        IFacets.

        """

        return facets_dict
    
    def organization_facets(
        self, facets_dict: typing.OrderedDict, group_type: str, package_type: str
    ) -> typing.OrderedDict:
        """IFacets interface requires reimplementation of all facets-related methods

        In this case we do not really need to override this method, but need to satisfy
        IFacets.

        """

        return facets_dict


def _parse_date(raw_date: str) -> typing.Optional[str]:
    """Parse user-submitted date into a string usable in Solr searches."""
    try:
        parsed_date = dateutil.parser.parse(raw_date, ignoretz=True).replace(
            tzinfo=dt.timezone.utc
        )
        result = parsed_date.isoformat().replace("+00:00", "Z")
    except dateutil.parser.ParserError:
        logger.exception("Could not parse date from input string")
        result = None
    return result
