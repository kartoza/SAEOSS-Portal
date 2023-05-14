import enum
import typing

ISO_TOPIC_CATEGORIES: typing.Final[typing.List[typing.Tuple[str, str]]] = [
    ("farming", "Farming"),
    ("biota", "Biota"),
    ("boundaries", "Boundaries"),
    ("climatologyMeteorologyAtmosphere", "Climatology, Meteorology, Atmosphere"),
    ("economy", "Economy"),
    ("elevation", "Elevation"),
    ("environment", "Environment"),
    ("geoscientificInformation", "Geoscientific Information"),
    ("health", "Health"),
    ("imageryBaseMapsEarthCover", "Imagery, Basemaps, Earth Cover"),
    ("intelligenceMilitary", "Intelligence, Millitary"),
    ("inlandWaters", "Inland Waters"),
    ("location", "Location"),
    ("oceans", "Oceans"),
    ("planningCadastre", "Planning, Cadastre"),
    ("society", "Society"),
    ("structure", "Structure"),
    ("transportation", "Transportation"),
    ("utilitiesCommuinication", "Utilities, Communication"),
]

SANSA_ORG_NAME = "sansa"


class DatasetManagementActivityType(enum.Enum):
    REQUEST_MAINTENANCE = "requested dataset maintenance"
    REQUEST_PUBLICATION = "requested dataset publication"


DATASET_MINIMAL_SET_OF_FIELDS = [
    "title",
    "name",
    "notes",
    "responsible_party-0-individual_name",
    "responsible_party-0-role",
    "responsible_party-0-position_name",
    "dataset_reference_date-0-reference",
    "dataset_reference_date-0-reference_date_type",
    "topic_and_sasdi_theme-0-iso_topic_category",
    "owner_org",
    "private",
    "metadata_language_and_character_set-0-dataset_language",
    "metadata_language_and_character_set-0-metadata_language",
    "metadata_language_and_character_set-0-dataset_character_set",
    "metadata_language_and_character_set-0-metadata_character_set",
    "lineage_statement",
    "distribution_format-0-name",
    "distribution_format-0-version",
    "spatial",
    "spatial_parameters-0-equivalent_scale",
    "spatial_parameters-0-spatial_representation_type",
    "spatial_parameters-0-spatial_reference_system",
    "metadata_date",
]

DATASET_FULL_SET_OF_FIELDS = [
    "title",
    "name",
    "featured",
    "doi",
    "metadata_standard-0-name",
    "metadata_standard-0-version",
    "notes",
    "responsible_party-0-individual_name",
    "responsible_party-0-position_name",
    "responsible_party-0-role",
    "responsible_party-0-electronic_mail_address",
    "responsible_party_contact_address-0-delivery_point",
    "responsible_party_contact_address-0-city",
    "responsible_party_contact_address-0-administrative_area",
    "responsible_party_contact_address-0-postal_code",
    "responsible_party_contact_info-0-voice",
    "responsible_party_contact_info-0-facsimile",
    "contact-0-individual_name",
    "contact-0-position_name",
    "contact-0-role",
    "contact-0-electronic_mail_address",
    "contact_address-0-delivery_point",
    "contact_address-0-city",
    "contact_address-0-administrative_area",
    "contact_address-0-postal_code",
    "contact_information-0-voice",
    "contact_information-0-facsimile",
    "owner_org",
    "private",
    "dataset_reference_date-0-reference",
    "dataset_reference_date-0-reference_date_type",
    "topic_and_sasdi_theme-0-iso_topic_category",
    "topic_and_sasdi_theme-0-sasdi_theme",
    "tag_string",
    "metadata_record_format-0-name",
    "metadata_record_format-0-version",
    "metadata_language_and_character_set-0-dataset_language",
    "metadata_language_and_character_set-0-metadata_language",
    "metadata_language_and_character_set-0-dataset_character_set",
    "metadata_language_and_character_set-0-metadata_character_set",
    "lineage_statement",
    "distribution_format-0-name",
    "distribution_format-0-version",
    "online_resource-0-name",
    "online_resource-0-linkeage",
    "online_resource-0-description",
    "online_resource-0-application_profile",
    "spatial",
    "spatial_parameters-0-equivalent_scale",
    "spatial_parameters-0-spatial_representation_type",
    "spatial_parameters-0-spatial_reference_system",
    "reference_system_additional_info",
    "metadata_date",
]

XML_DATASET_NAMING_MAPPING = {
    "title": "title",
    "name": "name",
    "featured": "featured",
    "doi": "doi",
    "notes": "notes",
    "private": "private",
    "tagString": "tag_string",
    "MetadataStandardName": "metadata_standard-0-name",
    "MetadataStandardVersion": "metadata_standard-0-version",
    "OwnerOrg": "owner_org",
    "ResponsiblePartyIndividualName": "responsible_party-0-individual_name",
    "ResponsiblePartyRole": "responsible_party-0-role",
    "ResponsiblePartyPositionName": "responsible_party-0-position_name",
    "ResponsiblePartyElectronicMailAddress": "responsible_party-0-electronic_mail_address",
    "ResponsiblePartyContactAddressDeliveryPoint": "responsible_party_contact_address-0-delivery_point",
    "ResponsiblePartyContactAddressCity": "responsible_party_contact_address-0-city",
    "ResponsiblePartyContactAddressAdministrativeArea": "responsible_party_contact_address-0-administrative_area",
    "ResponsiblePartyContactAddressPostalCode": "responsible_party_contact_address-0-postal_code",
    "ResponsiblePartyContactInfoVoice": "responsible_party_contact_info-0-voice",
    "ResponsiblePartyContactInfoFacsimile": "responsible_party_contact_info-0-facsimile",
    "ReferenceDate": "dataset_reference_date-0-reference",
    "ReferenceDateType": "dataset_reference_date-0-reference_date_type",
    "IsoTopicCategory": "topic_and_sasdi_theme-0-iso_topic_category",
    "LineageStatement": "lineage_statement",
    "DatasetLanguage": "metadata_language_and_character_set-0-dataset_language",
    "MetadataLanguage": "metadata_language_and_character_set-0-metadata_language",
    "DatasetCharacterset": "metadata_language_and_character_set-0-dataset_character_set",
    "MetadataCharacterset": "metadata_language_and_character_set-0-metadata_character_set",
    "DistributionFormatName": "distribution_format-0-name",
    "DistributionFormatVersion": "distribution_format-0-version",
    "spatial": "spatial",
    "EquivalentScale": "spatial_parameters-0-equivalent_scale",
    "SpatialRepresentationType": "spatial_parameters-0-spatial_representation_type",
    "SpatialReferenceSystem": "spatial_parameters-0-spatial_reference_system",
    "StampDate": "metadata_date",
    "ContactIndividualName": "contact-0-individual_name",
    "ContactPositionName": "contact-0-position_name",
    "ContactRole": "contact-0-role",
    "ContactElectronicMailAddress": "contact-0-electronic_mail_address",
    "ContactAddressDeliveryPoint": "contact_address-0-delivery_point",
    "ContactAddressCity": "contact_address-0-city",
    "ContactAddressAdministrativeArea": "contact_address-0-administrative_area",
    "ContactAddressPostalCode": "contact_address-0-postal_code",
    "ContactInformationVoice": "contact_information-0-voice",
    "ContactInformationFacsimile": "contact_information-0-facsimile",
}

# this is necessary to ensure consistancy with saeon extra names

DATASET_SUBFIELDS_MAPPING = {
    "metadata_standard_name": "metadata_standard-0-name",
    "metadata_standard_version": "metadata_standard-0-version",
    "responsible_party_individual_name": "responsible_party-0-individual_name",
    "responsible_party_role": "responsible_party-0-role",
    "responsible_party_position_name": "responsible_party-0-position_name",
    "responsible_party_electronic_mail_address": "responsible_party-0-electronic_mail_address",
    "responsible_party_contact_address_delivery_point": "responsible_party_contact_address-0-delivery_point",
    "responsible_party_contact_address_city": "responsible_party_contact_address-0-city",
    "responsible_party_contact_address_administrative_area": "responsible_party_contact_address-0-administrative_area",
    "responsible_party_contact_address_postal_code": "responsible_party_contact_address-0-postal_code",
    "responsible_party_contact_info_voice": "responsible_party_contact_info-0-voice",
    "responsible_party_contact_info_facsimile": "responsible_party_contact_info-0-facsimile",
    "reference_date": "dataset_reference_date-0-reference",
    "reference_datetype": "dataset_reference_date-0-reference_date_type",
    "stamp_date": "metadata_date",
    "topic_category": "topic_and_sasdi_theme-0-iso_topic_category",
    "lineage_statement": "lineage",
    "dataset_language": "metadata_language_and_character_set-0-dataset_language",
    "metadata_language": "metadata_language_and_character_set-0-metadata_language",
    "dataset_character_set": "metadata_language_and_character_set-0-dataset_character_set",
    "metadata_character_set": "metadata_language_and_character_set-0-metadata_character_set",
    "format_name": "distribution_format-0-name",
    "format_version": "distribution_format-0-version",
    "equivalent_scale": "spatial_parameters-0-equivalent_scale",
    "spatial_representation_type": "spatial_parameters-0-spatial_representation_type",
    "spatial_reference_system": "spatial_parameters-0-spatial_reference_system",
    "contact_organisation": "contact-0-organisation_name",
    "contact_individual_name": "contact-0-individual_name",
    "contact_position_name": "contact-0-position_name",
    "contact_role": "contact-0-role",
    "contact_electronic_mail_address": "contact-0-electronic_mail_address",
    "contact_address_delivery_point": "contact_address-0-delivery_point",
    "contact_address_city": "contact_address-0-city",
    "contact_address_administrative_area": "contact_address-0-administrative_area",
    "contact_address_postal_code": "contact_address-0-postal_code",
    "contact_information_voice": "contact_information-0-voice",
    "contact_information_facsimile": "contact_information-0-facsimile",
}



DATASET_Harvest_MINIMAL_SET_OF_FIELDS_MAPPING = {
    "guid":"id",
    "id":"id",
    "title":"title",
    "name":"name",
    "metadata_standard_name":"metadata_standard-0-name",
    "metadata_standard_version":"metadata_standard-0-version",
    "notes":"notes",
    "owner_org":"owner_org",
    "responsible_party_individual_name":"responsible_party-0-individual_name",
    "responsible_party_role":"responsible_party-0-role",
    "topic_category":"topic_and_sasdi_theme-0-iso_topic_category",
    "dataset_language":"metadata_language_and_character_set-0-dataset_language",
    "metadata_language":"metadata_language_and_character_set-0-metadata_language",
    "dataset_character_set":"metadata_language_and_character_set-0-dataset_character_set",
    "metadata_character_set":"metadata_language_and_character_set-0-metadata_character_set",
    "lineage":"lineage",
    "contact_organisation": "contact-0-organisation_name",
    "contact_individual_name": "contact-0-individual_name",
    "distribution_format_name":"distribution_format-0-name",
    "distribution_format_version":"distribution_format-0-version",
    "spatial":"spatial",
    "equivalent_scale":"spatial_parameters-0-equivalent_scale",
    "representation_type":"spatial_parameters-0-spatial_representation_type",
    "spatial_reference_system":"spatial_parameters-0-spatial_reference_system", # this needs handling
    "reference_date":"dataset_reference_date-0-reference",
    "dataset_reference_date":"dataset_reference_date-0-reference",
    "dataset_reference_date_type":"dataset_reference_date-0-reference_date_type",
    "metadata_date":"metadata_date",
}



class DCPRRequestRequiredFields(enum.Enum):
    DATASET_LANGUAGE = "en"
    DATASET_CHARACTER_SET = "ucs-2"
    METADATA_CHARACTER_SET = "ucs-2"
    DISTRIBUTION_FORMAT_NAME = "Electronic Metadata Record"
    DISTRIBUTION_FORMAT_VERSION = "1.0"
    EQUIVALENT_SCALE = "10"
    ISO_TOPIC_CATEGORY = "location"
    LINEAGE_LEVEL = "001"
    LINEAGE_STATEMENT = "Formed from a DCPR request"
    LINEAGE_PROCESS_DESCRIPTION = "Formed from a DCPR request"
    METADATA_LANGUAGE = "en"
    METADATA_STANDARD_NAME = "SANS 1878"
    METADATA_STANDARD_VERSION = "1.1"
    NOTES = "Default notes"
    PURPOSE = "Purpose"
    SPATIAL_REFERENCE_SYSTEM = "EPSG:4326"
    SPATIAL_REPRESENTATION_TYPE = "001"
    STATUS = "completed"
    REFERENCE_DATE_TYPE = "Creation"
    STAMP_DATE_TYPE = "Creation"
    RESPONSIBLE_PARTY_INDIVIDUAL_NAME = "individual_name"
    RESPONSIBLE_PARTY_POSITION_NAME = "dataset custodian"
    RESPONSIBLE_PARTY_ROLE = "originator"
