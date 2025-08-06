import logging
import typing
from datetime import datetime
import re

import requests
from ckan.lib.navl.dictization_functions import Missing

from ckan.plugins import toolkit
from ckan.lib.navl.dictization_functions import (
    Missing,
)  # note: imported for type hints only

from ckantoolkit import get_validator
import json
import jsonschema
from jsonschema import validate
import logging
import os
from .action import ckan_custom_actions
from stac_validator import stac_validator
from pystac.validation import validate_dict

ignore_missing = get_validator("ignore_missing")
logger = logging.getLogger(__name__)


def to_date_after_from_date_validator(key, flattened_data, errors, context):
    """Validator that checks that start and end dates are consistent"""
    logger.debug(f"{flattened_data=}")
    # ('reference_system_additional_info', 0, 'temporal_extent_period_duration_from')
    from_date = flattened_data[
        ("reference_system_additional_info", 0, "temporal_extent_period_duration_from")
    ]
    to_date = flattened_data[
        ("reference_system_additional_info", 0, "temporal_extent_period_duration_to")
    ]
    from_date = datetime.strptime(from_date, "%y-%m-%d")
    to_date = datetime.strptime(to_date, "%y-%m-%d")
    if to_date < from_date:
        raise toolkit.Invalid(
            toolkit._(
                "Please provide correct temporal duration for temporal references (from - to)"
            )
        )
    else:
        return ignore_missing(key, flattened_data, errors, context)


def value_or_true_validator(value: typing.Union[str, Missing]):
    """Validator that provides a default value of `True` when the input is None.

    This was designed with a package's `private` field in mind. We want it to be
    assigned a value of True when it is not explicitly provided on package creation.
    This shall enforce creating private packages by default.

    """

    logger.debug(f"inside value_or_true. Original value: {value!r}")
    return value if value != toolkit.missing else True


def srs_validator(value: str) -> str:
    """Validator for a dataset's spatial_reference_system field"""

    try:
        parsed_value = value.replace(" ", "").upper()
        if parsed_value.count(":") == 0:
            raise toolkit.Invalid(
                toolkit._("Please provide a colon-separated value, e.g. EPSG:4326")
            )
    except AttributeError:
        value = "EPSG:4326"

    try:
        authority, code = value.split(":")
    except ValueError:
        raise toolkit.Invalid(
            toolkit._(
                "Could not extract Spatial Reference System's authority and code. "
                "Please provide them as a colon-separated value, e.g. "
                "EPSG:4326"
            )
            % {"value": value}
        )

    return value


def lineage_source_srs_validator(value):
    """ "
    the difference from above method
    that the lineage source srs can
    be empty
    """
    if value == "":
        return ""
    else:
        srs_validator(value)


def version_validator(value):
    """
    check if the version is number or not
    """
    try:
        value = float(value)
    except:
        raise toolkit.Invalid("the dataset version should be a number")
    return value


def doi_validator(value: str):
    """
    check if the doi follows
    certain pattern.
    """
    if value == "" or value is None:
        return ""

    if type(value) is Missing:
        return ""

    pattern = "^10\\.\\d{4,}(\\.\\d+)*/[-._;()/:a-zA-Z0-9]+$"
    if re.match(pattern, value) is None:
        raise toolkit.Invalid(
            """
        doi is not in the correct form,
        please refer to https://www.doi.org/
        """
        )
    else:
        return value
    
def _stac_validator(jsonData):
    # if type == 'collection':
    #     file = os.path.abspath(os.path.dirname(__file__)) + "/stac_validators/collection/collection.json"
    # if type == 'catalog':
    #     file = os.path.abspath(os.path.dirname(__file__)) + "/stac_validators/catalog/catalog.json"
    # if type == 'item':
    #     file = os.path.abspath(os.path.dirname(__file__)) + "/stac_validators/item/item.json"
    # f = open(file)
    # schema = json.load(f)
    # try:
    #     validate(instance=jsonData, schema=schema)
    #     return
    # except jsonschema.exceptions.ValidationError as err:
    #     logging.debug(f"validation error {err}")
    #     raise ckan_custom_actions.ValidationError([f"The uploaded file does not follow STAC guidelines. Please ammend the following: \n\n{err}"],)
    stac = stac_validator.StacValidate(jsonData)
    stac.run()
    if stac.message[0]['valid_stac'] == True:
        return True
    else:
        # return dict(stac.message[0])
        raise ckan_custom_actions.ValidationError([f"The uploaded file does not follow STAC guidelines. Please ammend the following: \n\n{stac.message[0]}"],)
    

def validate_stac_json(stac_json: typing.Union[str, dict]) -> bool:
    """
    Validate a STAC JSON string or dict.
    
    Args:
        stac_json (str | dict): STAC JSON data as a string or dictionary.

    Returns:
        bool: True if valid, raises an error if invalid.
    """
    # Load JSON if it's a string
    if isinstance(stac_json, str):
        try:
            stac_data = json.loads(stac_json)
        except json.JSONDecodeError as e:
            raise ckan_custom_actions.ValidationError(f"Invalid JSON: {e}")
    else:
        stac_data = stac_json

    try:
        # This checks the JSON structure against the STAC schemas
        validate_dict(stac_data)
        return True
    except Exception as e:
        raise ckan_custom_actions.ValidationError([f"The file/link does not follow STAC guidelines. Errors: \n\n{e}"],)
    

def validate_stac_url(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ckan_custom_actions.ValidationError(
            [f"Failed to fetch the URL: {url}\nError: {e}"]
        )

    try:
        stac_data = response.json()
    except Exception as e:
        raise ckan_custom_actions.ValidationError(
            [f"Response content is not valid JSON: {e}"]
        )

    try:
        if "collections" in stac_data and isinstance(stac_data["collections"], list):
            # This is a STAC Catalog
            for i, collection in enumerate(stac_data["collections"]):
                try:
                    validate_dict(collection)
                except Exception as e:
                    raise ckan_custom_actions.ValidationError(
                        [f"STAC Catalog contains invalid collection at index {i}.\nErrors: {e}"]
                    )
            return "catalog"

        elif "extent" in stac_data and stac_data.get("type") == "Collection":
            # This is a STAC Collection
            try:
                validate_dict(stac_data)
                return "collection"
            except Exception as e:
                raise ckan_custom_actions.ValidationError(
                    [f"STAC Collection is invalid.\nErrors: {e}"]
                )

        elif stac_data.get("type") == "Feature" and "geometry" in stac_data:
            # This is a STAC Item
            try:
                validate_dict(stac_data)
                return "item"
            except Exception as e:
                raise ckan_custom_actions.ValidationError(
                    [f"STAC Item is invalid.\nErrors: {e}"]
                )

        else:
            raise ckan_custom_actions.ValidationError(
                ["The STAC JSON structure doesn't match Catalog, Collection, or Item."]
            )
    except Exception as e:
        raise ckan_custom_actions.ValidationError(
            [f"Validation error: {e}"]
        )




def stac_validator_admin(json_data):
    stac = stac_validator.StacValidate(json_data)
    stac.run()
    return dict(stac.message[0])
    
