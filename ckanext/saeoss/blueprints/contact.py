# -*- coding: utf-8 -*-
"""
A blueprint rendering contact page.
"""
from flask import Blueprint
from ckan.plugins import toolkit

contact_blueprint = Blueprint(
    "contact", __name__, template_folder="templates", url_prefix="/contact"
)


@contact_blueprint.route("/")
def index():
    """A blueprint rendering contact template.

    """
    return toolkit.render("contact.html")
