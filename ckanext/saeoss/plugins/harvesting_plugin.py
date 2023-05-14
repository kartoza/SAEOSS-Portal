import datetime as dt
import logging
import pathlib
import typing

import dateutil.parser
import langcodes
import yaml
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model.license import LicenseNotSpecified
from ckanext.spatial.interfaces import ISpatialHarvester
from ..cli import _CkanSaeossDataset, _CkanResource
from ..constants import DATASET_SUBFIELDS_MAPPING
from ..constants import DATASET_Harvest_MINIMAL_SET_OF_FIELDS_MAPPING
import re
import ast

logger = logging.getLogger(__name__)

class HarvestingPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    """Custom plugin to deal with harvesting-related customizations.

    This class exists in order to work around a bug in ckanext-spatial:

        https://github.com/ckan/ckanext-spatial/issues/277

    The mentioned bug prevents being able to have a CKAN extension plugin using both
    the `IValidators` and the `ISpatialHarvester` interfaces at the same time.

    As an alternative, we have implemented the current plugin class with the aim
    to use it strictly for customization of the harvesters (_i.e._ implement the
    ISpatialHarvester interface) while the main plugin class
    (saeoss_plugin.SaeossPlugin) is still handling all of the other SAEOSS
    customizations.

    """

    plugins.implements(ISpatialHarvester, inherit=True)

    def get_package_dict(
        self, context: typing.Dict, data_dict: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        """Extension point required by ISpatialHarvester"""
        package_dict = data_dict.get("package_dict", {})
        iso_values = data_dict.get("iso_values", {})
        parsed_resources = []
        for resource_dict in package_dict.get("resources", []):
            parsed_resources.append(
                _CkanResource(
                    url=resource_dict.get("url"),
                    format=resource_dict.get("format"),
                    format_version="change me",
                    name=resource_dict.get("name"),
                    description=resource_dict.get("description") or None,
                )
            )
        parsed_tags = []
        for parsed_tag in package_dict.get("tags", []):
            parsed_tags.append(
                {"name": parsed_tag.get("name", ""), "vocabulary_id": None}
            )
        # declared_dataset_language = _get_possibly_list_item(
        #     iso_values, "dataset-language"
        # )
        # dataset_language = _get_language_code(declared_dataset_language or "en")
        iso_topic_category = _get_possibly_list_item(iso_values, "topic-category")
        equivalent_scale = _get_possibly_list_item(iso_values, "equivalent-scale")

        package_dict = _get_extras_subfields(package_dict)

        dataset = _CkanSaeossDataset(
            type="dataset",
            private=True,
            featured=False,
            name=package_dict.get("name"),
            title=package_dict.get("title"),
            notes=package_dict.get("notes"),
            iso_topic_category=iso_topic_category or "",
            #owner_org=package_dict.get("owner_org"),
            owner_org="kartoza",
            maintainer=iso_values.get("contact"),
            maintainer_email=iso_values.get("contact-email"),
            license_id=LicenseNotSpecified.id,  # set this default and let publisher adjust
            spatial=_get_spatial_field(package_dict),
            resources=parsed_resources,
            tags=parsed_tags,
            source=None,
            version=None,
        )

        # for var in DATASET_Harvest_MINIMAL_SET_OF_FIELDS_MAPPING.values():
        #     setattr(dataset, var, None)
        
        new_data_dict = dataset.to_data_dict()
        new_data_dict.update(package_dict)
        # filers, remove these as you go
        new_data_dict["metadata_language_and_character_set-0-metadata_character_set"] = "ucs-2"
        new_data_dict["metadata_language_and_character_set-0-dataset_character_set"] = "ucs-2"
        new_data_dict["spatial_parameters-0-equivalent_scale"] = "5000"
        new_data_dict["spatial_parameters-0-spatial_representation_type"] = "001"
        del new_data_dict["extras"]

        new_data_dict["id"] = iso_values.get("guid")
        new_data_dict["metadata_modified"] = iso_values.get("date_updated")

        return new_data_dict


def _get_temporal_reference_date(iso_values: typing.Dict) -> str:
    """
    temporal reference date might be different 
    from the reference system, we are splitting
    the dates
    """
    #fallback_reference_date = dt.datetime.now(dt.timezone.utc).isoformat()

    fallback_reference_date = None
    if (raw_temp_extent_begin := iso_values.get("temporal-extent-begin")) is not None:
        if isinstance(raw_temp_extent_begin, list):
            try:
                temp_extent_begin = raw_temp_extent_begin[0]
            except IndexError:
                temp_extent_begin = None
        else:
            temp_extent_begin = raw_temp_extent_begin
        try:
            reference_date = dateutil.parser.parse(temp_extent_begin)
        except (TypeError, dateutil.parser.ParserError):
            logger.exception(msg=f"Could not parse {temp_extent_begin!r} as a datetime")
            result = fallback_reference_date
        else:
            result = reference_date.isoformat()
    else:
        for related_date in iso_values.get("dataset-reference-date", []):
            if related_date.get("type", "publication") == "creation":
                if (raw_date := related_date.get("value")) is not None:
                    try:
                        reference_date = dateutil.parser.parse(raw_date)
                    except dateutil.parser.ParserError:
                        logger.exception(
                            msg=f"Could not parse {raw_date!r} as a datetime"
                        )
                        result = fallback_reference_date
                    else:
                        result = reference_date.isoformat()
                break
        else:
            try:
                raw_date = iso_values["dataset-reference-date"][0]["value"]
                if raw_date is not None:
                    try:
                        reference_date = dateutil.parser.parse(raw_date)
                    except dateutil.parser.ParserError:
                        logger.exception(
                            msg=f"Could not parse {raw_date!r} as a datetime"
                        )
                        result = fallback_reference_date
                    else:
                        result = reference_date.isoformat()
            except (KeyError, IndexError):
                result = fallback_reference_date
    return result

def _get_spatial_field(package: typing.Dict):
    if package.get("extra") is not None:
        if package.get("extra").get("spatial") is not None:
            spatial = package.get("extra").get("spatial")
    else:
        spatial = toolkit.config.get(
            "ckan.saeoss.default_spatial_search_extent"
        )
    return spatial

def _get_allowed_dataset_languages() -> typing.List[str]:
    dataset_schema_path = (
        pathlib.Path(__file__).parents[1] / "scheming/dataset_schema.yaml"
    )
    result = []
    if dataset_schema_path.exists():
        dataset_schema = yaml.safe_load(dataset_schema_path.read_text())
        for field_params in dataset_schema.get("dataset_fields"):
            if field_params["field_name"] == "dataset_language":
                for choice in field_params.get("choices", []):
                    result.append(choice["value"])
    return result


def _get_language_code(source_code: str) -> str:
    allowed_choices = _get_allowed_dataset_languages()
    default_language_code = "en"
    result = default_language_code
    try:
        target_code = langcodes.standardize_tag(langcodes.Language(source_code))
    except ValueError:
        logger.exception(
            msg=(
                f"Could not recognize language code {source_code}, applying default "
                f"language code of {default_language_code}"
            )
        )
    else:
        result = default_language_code
        if target_code in allowed_choices:
            result = target_code
        else:
            logger.debug(
                f"language code {result} is not allowed, applying default language code "
                f"of {default_language_code}"
            )
    return result


def _get_extras_subfields(data_dict:dict):
    """
    fields with harvested data
    comes within an extra field
    in the form of 
    [{key:key:value:val}, {key:key, value:val}]
    we rely on the subfields mapping to
    extract these
    """
    missing_extras = []
    extras:list = data_dict.get("extras")

    if extras is None:
        return data_dict
    
    for extra in extras:
        _key = extra.get("key").replace("-","_")
        if _key not in DATASET_Harvest_MINIMAL_SET_OF_FIELDS_MAPPING:
            missing_extras.append(_key)
    data_dict = _assign_extra_values(data_dict)

    return data_dict

def _assign_extra_values(data_dict):
    """
    taking extra keys from
    extra dict and assigning them
    values 
    """
    extras = data_dict.get("extras")
    global _log
    if extras is None:
        return data_dict
    for extra in extras:
        _key = extra.get("key").replace("-","_")
        _value = extra.get("value")
        if DATASET_Harvest_MINIMAL_SET_OF_FIELDS_MAPPING.get(_key):
            if "reference_date" in _key:
                data_dict = get_dataset_reference_date(ast.literal_eval(_value),data_dict)
            elif "spatial_reference_system" in _key:
                data_dict[DATASET_Harvest_MINIMAL_SET_OF_FIELDS_MAPPING[_key]] = _get_spatial_reference_system(_value)
            else:
                data_dict[DATASET_Harvest_MINIMAL_SET_OF_FIELDS_MAPPING[_key]] = _value
        _log = True
    
    return data_dict


def get_dataset_reference_date(harvested_reference_date:list, data_dict: typing.Dict)-> typing.Dict:
    """
    the referece date can be more than one with
    different types (creation, revision, publication, ..etc.)
    """
    fallback_reference_date = None
    for idx,related_date in enumerate(harvested_reference_date):
        if (raw_date := related_date.get("value")) is not None:
            try:
                reference_date = dateutil.parser.parse(raw_date)
            except dateutil.parser.ParserError:
                logger.exception(
                    msg=f"Could not parse {raw_date!r} as a datetime"
                )
                result = fallback_reference_date
            else:
                result = reference_date.isoformat()
            # get the type
            reference_date_type = get_reference_date_type(related_date.get("type"))
            reference_date_key = _get_subfield_key("dataset_reference_date",idx)
            reference_date_type_key = _get_subfield_key("dataset_reference_date_type",idx)
            data_dict[reference_date_key] = result
            data_dict[reference_date_type_key] = reference_date_type

    return data_dict

def get_reference_date_type(dateType:str)->str:
    """
    with harvesters the data type comes as
    publication, revision, creation, ...
    we converts here to 001, 002, 003, ...
    """
    if dateType=="revision":
        return "003"
    
    elif dateType=="publication":
        return "002"

    elif dateType=="creation":
        return "001"

def _get_subfield_key(key:str, index:int):
    """
    handle the case where the scheming key
    is repeated subfield, i.e has -index- in it
    """
    if key=="dataset_reference_date":
        _key = DATASET_Harvest_MINIMAL_SET_OF_FIELDS_MAPPING.get("dataset_reference_date")
        
    elif key=="dataset_reference_date_type":
        _key = DATASET_Harvest_MINIMAL_SET_OF_FIELDS_MAPPING.get("dataset_reference_date_type")
    
    rep = f"-{index}-"

    if _key is not None:
        return  re.sub(r"-\d-" , rep , _key)


def _get_spatial_reference_system(reference_system:str)->str:
    """
    spatial reference system comes multiple forms as:
    EPSG:4326
    4326
    http://www.opengis.net/def/crs/EPSG/0/3057
    we need to extract and normalize them
    to the form EPSG:4326    
    """
    if reference_system is None:
        return ""
    elif "http" in reference_system:
        return "EPSG:" + reference_system.split("/")[-1]
    elif ":" in reference_system:
        return reference_system
    else:
        try :
            return f"EPSG:{int(reference_system)}"
        except ValueError:
            return reference_system


def _get_possibly_list_item(mapping: typing.Mapping, key: str) -> typing.Optional[str]:
    value = mapping.get(key)
    if isinstance(value, list):
        try:
            value = value[0]
        except IndexError:
            value = None
    return value