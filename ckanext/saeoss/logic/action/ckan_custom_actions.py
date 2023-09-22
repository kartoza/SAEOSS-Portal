# -*- coding: utf-8 -*-
import ckan.plugins.toolkit as toolkit
from ckan.common import config
import ckan.logic as logic
import os
import pathlib
import ckan.lib.uploader as uploader
from ckan.lib.helpers import flash_notice, redirect_to, full_current_url
from ckan.common import c
import logging
import ckan.plugins as plugins
from ..validators import stac_validator
import json
import yaml
from xmltodict3 import XmlTextToDict

logger = logging.getLogger(__name__)
# Define some shortcuts
# Ensure they are module-private so that they don't get loaded as available
# actions in the action API.
_check_access = logic.check_access
_get_action = logic.get_action
ValidationError = logic.ValidationError
NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
_get_or_bust = logic.get_or_bust


class Failed(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


@toolkit.chained_action
def resource_create(original_action, context: dict, data_dict: dict) -> dict:
    model = context['model']
    user = context['user']

    logger.debug(f"package create was called {data_dict}")

    package_id = _get_or_bust(data_dict, 'package_id')
    if not data_dict.get('url'):
        data_dict['url'] = ''

    pkg_dict = _get_action('package_show')(
        dict(context, return_type='dict'),
        {'id': package_id})

    _check_access('resource_create', context, data_dict)

    for plugin in plugins.PluginImplementations(plugins.IResourceController):
        plugin.before_create(context, data_dict)

    if 'resources' not in pkg_dict:
        pkg_dict['resources'] = []

    upload = uploader.get_resource_uploader(data_dict)

    if 'mimetype' not in data_dict:
        if hasattr(upload, 'mimetype'):
            data_dict['mimetype'] = upload.mimetype

    if 'size' not in data_dict:
        if hasattr(upload, 'filesize'):
            data_dict['size'] = upload.filesize

    if upload:
        if data_dict["resource_type"] == "stac":
            allowed_types = ["application/json", "application/xml", "application/yaml"]

            if upload.mimetype not in allowed_types:
                raise ValidationError(["Only json, yaml and xml files are allowed"])

            temp_file = upload.upload_file
            file_contents = temp_file.read()
            
            if upload.mimetype == "application/json":
                json_data = json.loads(file_contents)

            if upload.mimetype == "application/yaml":
                json_data = yaml.load(file_contents)

            if upload.mimetype == "application/xml":
                json_data = XmlTextToDict(file_contents, ignore_namespace=True).get_dict()
    
            stac_validator(json_data, data_dict["stac_specification"])

    pkg_dict['resources'].append(data_dict)

    try:
        context['defer_commit'] = True
        context['use_cache'] = False
        _get_action('package_update')(context, pkg_dict)
        context.pop('defer_commit')
    except ValidationError as e:
        try:
            raise ValidationError(e.error_dict['resources'][-1])
        except (KeyError, IndexError):
            raise ValidationError(e.error_dict)

    # Get out resource_id resource from model as it will not appear in
    # package_show until after commit
    upload.upload(context['package'].resources[-1].id,
                  uploader.get_max_resource_size())

    model.repo.commit()

    #  Run package show again to get out actual last_resource
    updated_pkg_dict = _get_action('package_show')(context, {'id': package_id})
    resource = updated_pkg_dict['resources'][-1]

    #  Add the default views to the new resource
    logic.get_action('resource_create_default_resource_views')(
        {'model': context['model'],
         'user': context['user'],
         'ignore_auth': True
         },
        {'resource': resource,
         'package': updated_pkg_dict
         })

    for plugin in plugins.PluginImplementations(plugins.IResourceController):
        plugin.after_create(context, resource)

    return resource


@toolkit.chained_action
def resource_update(original_action, context: dict, data_dict: dict):
    '''Update a resource.

    To update a resource you must be authorized to update the dataset that the
    resource belongs to.

    .. note:: Update methods may delete parameters not explicitly provided in the
        data_dict. If you want to edit only a specific attribute use `resource_patch`
        instead.

    For further parameters see
    :py:func:`~ckan.logic.action.create.resource_create`.

    :param id: the id of the resource to update
    :type id: string

    :returns: the updated resource
    :rtype: string

    '''

    logger.debug("package update", data_dict)

    model = context['model']
    id = _get_or_bust(data_dict, "id")

    if not data_dict.get('url'):
        data_dict['url'] = ''

    logger.debug("resource update", data_dict)

    if "http" not in data_dict["url"] and "https" not in data_dict["url"]:

        if data_dict["updated_text"]:
            first_folder = id[0:3]
            second_folder = id[3:6]
            file_name = id[6:len(id)]

            upload = f"/home/appuser/data/resources/{first_folder}/{second_folder}/{file_name}"

            logger.debug(f"resource update custom {data_dict}")
            f = open(upload, "w")
            f.write(data_dict["updated_text"])
            f.close()

            del data_dict["updated_text"]

    resource = model.Resource.get(id)
    context["resource"] = resource
    old_resource_format = resource.format

    if not resource:
        logger.debug('Could not find resource %s', id)
        raise NotFound(_('Resource was not found.'))

    _check_access('resource_update', context, data_dict)
    del context["resource"]

    package_id = resource.package.id
    pkg_dict = _get_action('package_show')(dict(context, return_type='dict'),
                                           {'id': package_id})

    for n, p in enumerate(pkg_dict['resources']):
        if p['id'] == id:
            break
    else:
        logger.error('Could not find resource %s after all', id)
        raise NotFound(_('Resource was not found.'))

    # Persist the datastore_active extra if already present and not provided
    if ('datastore_active' in resource.extras and
            'datastore_active' not in data_dict):
        data_dict['datastore_active'] = resource.extras['datastore_active']

    for plugin in plugins.PluginImplementations(plugins.IResourceController):
        plugin.before_update(context, pkg_dict['resources'][n], data_dict)

    pkg_dict['resources'][n] = data_dict

    try:
        context['use_cache'] = False
        updated_pkg_dict = _get_action('package_update')(context, pkg_dict)
    except ValidationError as e:
        try:
            raise ValidationError(e.error_dict['resources'][n])
        except (KeyError, IndexError):
            raise ValidationError(e.error_dict)

    resource = _get_action('resource_show')(context, {'id': id})

    if old_resource_format != resource['format']:
        _get_action('resource_create_default_resource_views')(
            {'model': context['model'], 'user': context['user'],
             'ignore_auth': True},
            {'package': updated_pkg_dict,
             'resource': resource})

    for plugin in plugins.PluginImplementations(plugins.IResourceController):
        plugin.after_update(context, resource)

    return resource
