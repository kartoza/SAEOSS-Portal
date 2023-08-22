import typing
import pytest
from ckanext.saeoss.logic.action.ckan import _get_reference_date

pytestmark = pytest.mark.unit

PACKAGE_DICT_NO_REFERENCE_DATE = {
    'id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
    'name': 'c7eea7e1-b159-594b-bc0a-eef242b70334',
    'title': 'c7eea7e1-b159-594b-bc0a-eef242b70334',
    'version': None,
    'url': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'notes': 'Configure stac endpoint information in your Explorer `settings.env.py` file',
    'license_id': None,
    'type': 'dataset',
    'owner_org': '20cce4e7-b40d-4937-b5df-5e2b319209c6',
    'creator_user_id': 'b66f7683-4d92-479b-98c3-7a0da8bd9291',
    'metadata_created': '2023-08-21T07:13:43.248825',
    'metadata_modified': '2023-08-21T07:13:43.248832',
    'private': False,
    'state': 'active',
    'resources': [],
    'num_resources': 0,
    'tags': [],
    'num_tags': 0,
    'extras': [],
    'groups': [],
    'organization': {
        'id': '20cce4e7-b40d-4937-b5df-5e2b319209c6',
        'name': 'kartoza',
        'title': 'kartoza',
        'type': 'organization',
        'description': '',
        'image_url': '',
        'created': '2023-08-17T12:59:39.523043',
        'is_organization': True,
        'approval_status': 'approved',
        'state': 'active'
    },
    'relationships_as_subject': [],
    'relationships_as_object': [],
    'isopen': False,
    'license_title': None
}


PACKAGE_DICT_REFERENCE_DATE_EXTRAS = {
    'id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
    'name': 'c7eea7e1-b159-594b-bc0a-eef242b70334',
    'title': 'c7eea7e1-b159-594b-bc0a-eef242b70334',
    'version': None,
    'url': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'notes': 'Configure stac endpoint information in your Explorer `settings.env.py` file',
    'license_id': None,
    'type': 'dataset',
    'owner_org': '20cce4e7-b40d-4937-b5df-5e2b319209c6',
    'creator_user_id': 'b66f7683-4d92-479b-98c3-7a0da8bd9291',
    'metadata_created': '2023-08-21T07:13:43.248825',
    'metadata_modified': '2023-08-21T07:13:43.248832',
    'private': False,
    'state': 'active',
    'resources': [],
    'num_resources': 0,
    'tags': [],
    'num_tags': 0,
    'extras': [{
        'id': '0668083b-ae06-427d-bb46-d69e60eef5c2',
        'package_id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
        'key': 'dataset_reference_date',
        'value': '[{"reference": "2022-01-05", "reference_date_type": 1}]',
        'state': 'active'
    }, {
        'id': 'c5900a3a-da52-4881-a20a-be06f9bb61ee',
        'package_id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
        'key': 'distribution_format',
        'value': '[{"name": "distribution format", "version": "1.0"}]',
        'state': 'active'
    }, {
        'id': '8d0ad8d4-3b45-41f4-987a-c3fc07b502b2',
        'package_id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
        'key': 'doi',
        'value': '',
        'state': 'active'
    }, {
        'id': '0680f075-1602-42dc-a00a-de0473cb8379',
        'package_id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
        'key': 'featured',
        'value': 'false',
        'state': 'active'
    }, {
        'id': '4fbb9ba3-9af5-4c8f-9f07-5eed759631fa',
        'package_id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
        'key': 'lineage',
        'value': 'lineage statement',
        'state': 'active'
    }, {
        'id': '6f71c703-927c-45c8-875c-3022196fdbe1',
        'package_id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
        'key': 'metadata_date',
        'value': 'metadata',
        'state': 'active'
    }, {
        'id': '24597455-382f-4a94-8281-d98e8eab61c9',
        'package_id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
        'key': 'metadata_language_and_character_set',
        'value': '[{"dataset_character_set": "utf-8", "dataset_language": "en", "metadata_character_set": "utf-8", "metadata_language": "en"}]',
        'state': 'active'
    }, {
        'id': '6f1ce695-46cc-4074-b5e4-ab5c5689b70e',
        'package_id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
        'key': 'responsible_party',
        'value': '[{"individual_name": "responsible individual name", "position_name": "position name", "role": "owner"}]',
        'state': 'active'
    }, {
        'id': '1ba36a77-0ce7-401c-8fa8-676f99d70a29',
        'package_id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
        'key': 'spatial',
        'value': '{"type": "Polygon", "coordinates": [[[16.4699, -34.8212], [32.8931, -34.8212], [32.8931, -22.1265], [16.4699, -22.1265], [16.4699, -34.8212]]]}',
        'state': 'active'
    }, {
        'id': '16fcdf47-ea4c-410c-92be-79adcb33e08e',
        'package_id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
        'key': 'spatial_parameters',
        'value': '[{"equivalent_scale": "equivalent scale", "spatial_reference_system": "EPSG:3456", "spatial_representation_type": "001"}]',
        'state': 'active'
    }],
    'groups': [],
    'organization': {
        'id': '20cce4e7-b40d-4937-b5df-5e2b319209c6',
        'name': 'kartoza',
        'title': 'kartoza',
        'type': 'organization',
        'description': '',
        'image_url': '',
        'created': '2023-08-17T12:59:39.523043',
        'is_organization': True,
        'approval_status': 'approved',
        'state': 'active'
    },
    'relationships_as_subject': [],
    'relationships_as_object': [],
    'isopen': False,
    'license_title': None
}


PACKAGE_DICT_REFERENCE_DATE = {
    'id': 'DEAfrica_datac7eea7e1-b159-594b-bc0a-eef242b70334',
    'name': 'c7eea7e1-b159-594b-bc0a-eef242b70334',
    'title': 'c7eea7e1-b159-594b-bc0a-eef242b70334',
    'version': None,
    'url': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'notes': 'Configure stac endpoint information in your Explorer `settings.env.py` file',
    'license_id': None,
    'type': 'dataset',
    'owner_org': '20cce4e7-b40d-4937-b5df-5e2b319209c6',
    'creator_user_id': 'b66f7683-4d92-479b-98c3-7a0da8bd9291',
    'metadata_created': '2023-08-21T07:13:43.248825',
    'metadata_modified': '2023-08-21T07:13:43.248832',
    'private': False,
    'state': 'active',
    'resources': [],
    'num_resources': 0,
    'tags': [],
    'num_tags': 0,
    'dataset_reference_date': [
        {"reference": "2022-01-05", "reference_date_type": 1}
    ],
    'groups': [],
    'organization': {
        'id': '20cce4e7-b40d-4937-b5df-5e2b319209c6',
        'name': 'kartoza',
        'title': 'kartoza',
        'type': 'organization',
        'description': '',
        'image_url': '',
        'created': '2023-08-17T12:59:39.523043',
        'is_organization': True,
        'approval_status': 'approved',
        'state': 'active'
    },
    'relationships_as_subject': [],
    'relationships_as_object': [],
    'isopen': False,
    'license_title': None
}


@pytest.mark.parametrize(
    "package_dict, expected",
    [
        pytest.param(PACKAGE_DICT_REFERENCE_DATE, '2022-01-05'),
        pytest.param(PACKAGE_DICT_REFERENCE_DATE_EXTRAS, '2022-01-05'),
        pytest.param(PACKAGE_DICT_NO_REFERENCE_DATE, None)
    ],
)
def test_get_reference_date(package_dict: typing.Dict, expected):
    reference_date = _get_reference_date(package_dict)
    assert reference_date == expected
