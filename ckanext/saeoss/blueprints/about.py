# -*- coding: utf-8 -*-
"""
A blueprint rendering about page.
"""
from flask import Blueprint
from ckan.plugins import toolkit

about_blueprint = Blueprint(
    "about", __name__, template_folder="templates", url_prefix="/about"
)


@about_blueprint.route("/")
def index():
    """A blueprint rendering map template.

    """
    return toolkit.render("home/about.html")