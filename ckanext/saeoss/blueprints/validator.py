# -*- coding: utf-8 -*-
"""
A blueprint rendering map page.
"""
import logging
import typing

from flask import Blueprint, redirect, url_for, request
from ckan.plugins import toolkit
from ckan import model
from ..logic.validators import stac_validator_admin
import json
import yaml
from xmltodict3 import XmlTextToDict
import urllib

logger = logging.getLogger(__name__)

validator_blueprint = Blueprint(
    "validator", __name__, template_folder="templates", url_prefix="/validator"
)


@validator_blueprint.route("/", methods = ['POST', 'GET'])
def index():
    """A blueprint validation template.

    """
    return toolkit.render("validator/index.html",)

@validator_blueprint.route("/retrieve_metadata/", methods = ['POST', 'GET'])
def retrieve_metadata():
    if request.method == 'GET':
        data = []

        query = f""" SELECT id, name FROM package """
        package_result = model.Session.execute(query)

        for package in package_result:
            package_id = package[0]
            package_name = package[1]
            resource_list = []

            q = f""" SELECT id, url, package_id, format, url_type, name, extras FROM resource WHERE package_id = '{package_id}' """
            result = model.Session.execute(q)
            for x in result:
                id = x[0]
                url = x[1]
                package_id = x[2]
                format = x[3]
                url_type = x[4]
                resource_name  = x[5]
                extras = json.loads(x[6])
                data.append({
                    "package_id": package_id,
                    "package_name": package_name,
                    "resources": resource_list,
                    "resource_id": id,
                    "url": url,
                    "format": format,
                    "url_type": url_type,
                    "resource_name": resource_name,
                    "extras": extras
                })
        return json.dumps(data)


def _validate(context: typing.Dict, result: typing.List[typing.List[typing.Any]]):
    for x in result:
        resource_id = x[0]
        url = x[1]
        package_id = x[2]
        format = x[3]
        url_type = x[4]
        resource_name = x[5]
        extras = json.loads(x[6])
        first_folder = resource_id[0:3]
        second_folder = resource_id[3:6]
        file_name = resource_id[6:len(resource_id)]

        query = f""" SELECT name FROM package WHERE id = '{package_id}' """
        package_result = model.Session.execute(query)

        for res in package_result:
            package_name = res[0]

        logger.debug(f'url_type: {url_type}')
        logger.debug(f'format {format}')
        json_data = None

        if url_type == 'upload' and format in ['json', 'yaml', 'xml']:
            file_url = f"/home/appuser/data/resources/{first_folder}/{second_folder}/{file_name}"
            file_contents = open(file_url, 'r').read()

            if format.lower() == "json":
                json_data = json.loads(file_contents)

            if format.lower() == "yaml":
                json_data = yaml.load(file_contents)

            if format.lower() == "xml":
                json_data = XmlTextToDict(file_contents, ignore_namespace=True).get_dict()
        elif url_type not in ['upload', 'datastore']:
            resp = urllib.request.urlopen(url)
            json_data = json.loads(resp.read())

        if format not in ['json', 'yaml', 'xml']:
            result = True
        else:
            result = stac_validator_admin(json_data, extras["stac_specification"])

        if result is not True:
            context["invalid"].append(resource_id)
        else:
            context["valid"].append(resource_id)
    return context

@validator_blueprint.route("/validate_all/", methods = ['POST', 'GET'])
def validate_all():
    context = {"valid": [], "invalid": []}

    if request.method == 'POST':

        q = f""" SELECT id, url, package_id, format, url_type, name, extras FROM resource """
        result = model.Session.execute(q)
        context = _validate(context, result)
        
    return json.dumps(context)

@validator_blueprint.route("/validate_selection/", methods = ['POST', 'GET'])
def validate_selection():
    context = {"valid": [], "invalid": []}

    if request.method == 'POST':
        data = request.get_json()
        logger.debug(f"json data {data}")
            
        for _data in data["value"]:

            q = f""" SELECT id, url, package_id, format, url_type, name, extras FROM resource  WHERE id = '{_data}'"""
            result = model.Session.execute(q)
            context = _validate(context, result)
    return json.dumps(context)