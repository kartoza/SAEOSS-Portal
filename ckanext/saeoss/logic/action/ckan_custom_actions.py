# -*- coding: utf-8 -*-
import requests
import ckan.plugins.toolkit as toolkit
from ckan.common import config
import ckan.logic as logic
import os
import pathlib
import ckan.lib.uploader as uploader
from ckan.lib.helpers import flash_notice, redirect_to, full_current_url
from ckan.common import c, g
import logging
import ckan.plugins as plugins
from ..validators import validate_stac_json, validate_stac_url
import json
import yaml
import xmltodict
from urllib.request import urlopen
from ckan.logic.action.create import _group_or_org_create
import ckan.model as model


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
    
    mimeNotAllowed = [
                    "text/html", 
                    "application/java", 
                    "application/java-byte-code", 
                    "application/x-javascript", 
                    "application/javascript", 
                    "application/ecmascript", 
                    "text/javascript", 
                    "text/ecmascript",
                    "application/octet-stream",
                    "text/x-server-parsed-html"
                ]

    if upload.mimetype in mimeNotAllowed:
        raise ValidationError([f"Mimetype {upload.mimetype} is not allowed!"])

    if 'size' not in data_dict:
        if hasattr(upload, 'filesize'):
            data_dict['size'] = upload.filesize

    if upload.mimetype == None:
        if data_dict['url'] == '':
            return {} 
            # raise ValidationError(["Please upload a file or link to an online resource"])

    if upload:
        if data_dict.get("resource_type") == "stac":
            if 'https' in data_dict['url'] or 'http' in data_dict['url']:
                validate_stac_url(data_dict['url'])
                

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

    model = context['model']
    id = _get_or_bust(data_dict, "id")

    if not data_dict.get('url'):
        data_dict['url'] = ''

    # if "http" not in data_dict["url"] and "https" not in data_dict["url"]:
    #
    #     if data_dict["updated_text"]:
    #         first_folder = id[0:3]
    #         second_folder = id[3:6]
    #         file_name = id[6:len(id)]
    #
    #         upload = f"/home/appuser/data/resources/{first_folder}/{second_folder}/{file_name}"
    #
    #         logger.debug(f"resource update custom {data_dict}")
    #         f = open(upload, "w")
    #         f.write(data_dict["updated_text"])
    #         f.close()
    #
    #         del data_dict["updated_text"]

    resource = model.Resource.get(id)
    context["resource"] = resource
    old_resource_format = resource.format

    if not resource:
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

@toolkit.chained_action
def organization_create(original_action, context: dict, data_dict: dict):
    '''Create a new organization.

    You must be authorized to create organizations.

    Plugins may change the parameters of this function depending on the value
    of the ``type`` parameter, see the
    :py:class:`~ckan.plugins.interfaces.IGroupForm` plugin interface.

    :param name: the name of the organization, a string between 2 and
        100 characters long, containing only lowercase alphanumeric
        characters, ``-`` and ``_``
    :type name: string
    :param id: the id of the organization (optional)
    :type id: string
    :param title: the title of the organization (optional)
    :type title: string
    :param description: the description of the organization (optional)
    :type description: string
    :param image_url: the URL to an image to be displayed on the
        organization's page (optional)
    :type image_url: string
    :param state: the current state of the organization, e.g. ``'active'`` or
        ``'deleted'``, only active organizations show up in search results and
        other lists of organizations, this parameter will be ignored if you
        are not authorized to change the state of the organization
        (optional, default: ``'active'``)
    :type state: string
    :param approval_status: (optional)
    :type approval_status: string
    :param extras: the organization's extras (optional), extras are arbitrary
        (key: value) metadata items that can be added to organizations,
        each extra
        dictionary should have keys ``'key'`` (a string), ``'value'`` (a
        string), and optionally ``'deleted'``
    :type extras: list of dataset extra dictionaries
    :param packages: the datasets (packages) that belong to the organization,
        a list of dictionaries each with keys ``'name'`` (string, the id
        or name of the dataset) and optionally ``'title'`` (string, the
        title of the dataset)
    :type packages: list of dictionaries
    :param users: the users that belong to the organization, a list
        of dictionaries each with key ``'name'`` (string, the id or name
        of the user) and optionally ``'capacity'`` (string, the capacity
        in which the user is a member of the organization)
    :type users: list of dictionaries

    :returns: the newly created organization (unless 'return_id_only' is set
              to True in the context, in which case just the organization id
              will be returned)
    :rtype: dictionary

    '''
    # wrapper for creating organizations
    context['ignore_auth'] = True
    data_dict.setdefault('type', 'organization')
    return original_action(context, data_dict)


