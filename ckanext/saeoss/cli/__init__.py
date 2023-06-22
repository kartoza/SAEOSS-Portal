import dataclasses
import logging
import typing
import uuid
import collections.abc
from pathlib import Path
from ..constants import DATASET_SUBFIELDS_MAPPING

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class _CkanBootstrapOrganization:
    name: str
    title: str
    description: str
    image_url: typing.Optional[Path] = None


@dataclasses.dataclass
class _CkanBootstrapUser:
    name: str
    email: str
    password: str


@dataclasses.dataclass
class _CkanBootstrapHarvester:
    name: str
    url: str
    source_type: str
    update_frequency: str
    configuration: typing.Dict


@dataclasses.dataclass
class _CkanResource:
    url: str
    format: str
    format_version: str
    package_id: typing.Optional[str] = None
    name: typing.Optional[str] = None
    description: typing.Optional[str] = None
    resource_type: typing.Optional[str] = None

    def to_data_dict(self) -> typing.Dict:
        result = {}
        for name, value in vars(self).items():
            if value is not None:
                result[name] = _to_data_dict(value)
        return result


@dataclasses.dataclass
class _CkanSaeossDataset:
    name: str
    private: bool
    notes: str
    iso_topic_category: str
    owner_org: str
    maintainer: str
    resources: typing.List
    spatial: str
    title: typing.Optional[str] = None
    maintainer_email: typing.Optional[str] = None
    type: typing.Optional[str] = "dataset"
    tags: typing.List[typing.Dict] = dataclasses.field(default_factory=list)
    source: typing.Optional[str] = None
    license_id: typing.Optional[str] = None
    version: typing.Optional[str] = None
    featured: typing.Optional[bool] = False
        
    def to_data_dict(self) -> typing.Dict:
        result = {}
        for name, value in vars(self).items():
            if value is not None:
                result[name] = _to_data_dict(value)
        if result.get("title") is None:
            result["title"] = self.name
        else:
            result["name"] = self.title

        return result


@dataclasses.dataclass
class _CkanExtBootstrapPage:
    name: str
    content: str
    private: bool
    org_id: typing.Optional[str] = None
    order: typing.Optional[str] = ""
    page_type: typing.Optional[str] = "page"
    user_id: typing.Optional[str] = None

    def to_data_dict(self) -> typing.Dict:
        result = {}
        for name, value in vars(self).items():
            if value is not None:
                result[name] = _to_data_dict(value)
        result["title"] = self.name.capitalize()
        return result


def _to_data_dict(value):
    if isinstance(value, (str, int, float)):
        result = value
    elif isinstance(value, collections.abc.Mapping):
        result = value
    elif isinstance(value, collections.abc.Iterable):
        result = [_to_data_dict(i) for i in value]
    elif getattr(value, "to_data_dict", None) is not None:
        result = value.to_data_dict()
    else:
        result = _to_data_dict(value)
    return result


@dataclasses.dataclass
class StacItem:
    id: str
    owner_org: str
    title: str
    name: str
    notes: str
    responsible_party_individual_name: str
    responsible_party_role: str
    responsible_party_position_name: str
    dataset_reference_date_reference: str
    dataset_reference_date_reference_date_type: str
    private: bool
    metadata_language_and_character_set_dataset_language: str
    metadata_language_and_character_set_metadata_language: str
    metadata_language_and_character_set_dataset_character_set: str
    metadata_language_and_character_set_metadata_character_set: str
    lineage: str
    distribution_format_name: str
    distribution_format_version: str
    topic_and_sasdi_theme_iso_topic_category: str
    spatial: str
    spatial_parameters_spatial_representation_type: str
    spatial_parameters_spatial_resolution: str
    spatial_parameters_equivalent_scale: str
    resources: typing.List    
    assetlink: str

    def to_data_dict(self) -> typing.Dict:
        """ creates Dictionary from StacItem object
            temporarly provides default values
            for missed sans fields 
        """
        
        pass
        # for link in item1.links:
        #     if link.rel == "thumbnail":
        #         data_dict["resources"].append({"name":link.target,"url":link.target, "format": "jpg", "format_version": "1.0"})
