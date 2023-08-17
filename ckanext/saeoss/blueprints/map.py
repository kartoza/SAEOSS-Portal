# -*- coding: utf-8 -*-
"""
A blueprint rendering map page.
"""
from flask import Blueprint
from ckan.plugins import toolkit

map_blueprint = Blueprint(
    "map", __name__, template_folder="templates", url_prefix="/map"
)


@map_blueprint.route("/")
def index():
    """A blueprint rendering map template.

    """
    return toolkit.render("map/map.html")
