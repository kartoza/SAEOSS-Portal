# -*- coding: utf-8 -*-
"""
A blueprint rendering stac harvest page.
"""
import json
import logging

from ckan import model
from ckan.common import c
from ckan.plugins import toolkit
from flask import Blueprint, request

from ckanext.saeoss.cli.commands import create_stac_dataset_func

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

        try:
            number_records = int(number_records)
        except:
            number_records = 10
            logger.info("number_records is not an integer, setting it to 10")

        logger.debug(user)
        logger.debug(url)
        logger.debug(owner_org)
        logger.debug(number_records)
        create_stac_dataset_func(user, url, owner_org, number_records)
                    
        return json.dumps({"message": "finished"})
    
    return json.dumps({"message": "empty request"})
