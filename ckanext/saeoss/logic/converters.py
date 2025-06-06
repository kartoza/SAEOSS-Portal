import json
import logging
from copy import deepcopy
from ckan.plugins import toolkit
from ckan.common import _
import ckan.lib.navl.dictization_functions as df

Invalid = df.Invalid

import datetime

from ckan.common import _
import ckan.lib.navl.dictization_functions as df

Invalid = df.Invalid

logger = logging.getLogger(__name__)


def bbox_converter(value: str) -> str:
    error_msg = toolkit._(
        "Invalid bounding box. Please provide a comma-separated list of values "
        "with upper left lat, upper left lon, lower right lat, lower right lon."
    )

    try:
        parsed_value = json.loads(value)
        if parsed_value.get("type") != "Polygon":
            raise toolkit.Invalid("Only GeoJSON Polygon bounding boxes are supported.")
        coordinates = parsed_value["coordinates"][0]
        upper_lat = coordinates[2][1]
        left_lon = coordinates[0][0]
        lower_lat = coordinates[0][1]
        right_lon = coordinates[1][0]
    except json.JSONDecodeError:
        try:
            bbox_coords = [float(i.strip()) for i in value.split(",")]
            if len(bbox_coords) != 4:
                raise toolkit.Invalid(error_msg)
            upper_lat, left_lon, lower_lat, right_lon = bbox_coords
        except ValueError:
            logger.exception("BBox parsing failed. Input was not valid float coordinates.")
            raise toolkit.Invalid(error_msg)
    except (IndexError, TypeError, AttributeError) as e:
        logger.exception("Invalid structure in bbox GeoJSON or string format.")
        raise toolkit.Invalid(error_msg)

    parsed = {
        "type": "Polygon",
        "coordinates": [
            [
                [left_lon, lower_lat],
                [right_lon, lower_lat],
                [right_lon, upper_lat],
                [left_lon, upper_lat],
                [left_lon, lower_lat],
            ]
        ],
    }
    return json.dumps(parsed)



def spatial_resolution_converter(value: str):
    """
    the natural numbers validator used with
    spatial resolution field causes
    internal server error when the type
    is None, handled here
    """
    if value == "":
        return -1
    return value

def convert_choices_select_to_int(data_dict, context):
    """
    while submitting the select choices numerical
    values, they are returned as strings,
    they should be submitted as ints, otherwises
    a value error would be raised.
    """
    # TODO: adding the field name for proper loggin

    logger.debug("convert select choices to int ")
    if data_dict == "":
        return ""
    try:
        return int(data_dict)
    except:
        raise toolkit.Invalid("select field should have a string value")


def check_if_number(data_dict):
    """
    check if the given value can be
    converted to a number
    """
    logger.debug("convert to real number ")
    if data_dict == "":
        return ""
    try:
        return float(data_dict)
    except:
        raise toolkit.Invalid("select field should be a number ")


def check_if_int(data_dict):
    """
    check if the given value can be
    converted to an integer
    """
    logger.debug("convert to int ")
    if data_dict == "":
        return ""
    try:
        return int(data_dict)
    except:
        raise toolkit.Invalid("select field should be an integer ")


def convert_select_custom_choice_to_extra(data_dict):
    """
    adding custom field to select options,
    currently appears as "__extras" in the
    database,
    """
    return data_dict


def default_metadata_standard_name(value):
    """
    returns SANS1878 as the default
    metadata standard name.
    """
    if value == "":
        return "SANS 1878-1:2011"


def default_metadata_standard_version(value):
    """
    returns SANS1878 as the default
    metadata standard name.
    """
    if value == "":
        return "1.1"
