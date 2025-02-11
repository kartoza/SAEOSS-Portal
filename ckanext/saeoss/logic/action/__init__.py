import typing

from ckan.logic.schema import validator_args

from ckan.plugins import toolkit

from ...constants import (
    DatasetManagementActivityType,
)

@validator_args
def default_create_activity_schema(
        ignore, not_missing, not_empty, unicode_safe,
        convert_user_name_or_id_to_id, object_id_validator,
        activity_type_exists, ignore_empty, ignore_missing):
    return {
        'id': [ignore],
        'timestamp': [ignore],
        'user_id': [not_missing, not_empty, unicode_safe,
                    convert_user_name_or_id_to_id],
        'object_id': [
            not_missing, not_empty, unicode_safe, object_id_validator],
        'activity_type': [not_missing, not_empty, unicode_safe,
                          activity_type_exists],
        'data': [ignore_empty, ignore_missing],
    }

def create_dataset_management_activity(
    dataset_id: str, activity_type: DatasetManagementActivityType
) -> typing.Dict:
    """
    This is a hacky way to relax the activity type schema validation
    we remove the default activity_type_exists validator because it is not possible
    to extend it with a custom activity
    """

    activity_schema = default_create_activity_schema()
    to_remove = None
    for index, validator in enumerate(activity_schema["activity_type"]):
        if validator.__name__ == "activity_type_exists":
            to_remove = validator
            break
    if to_remove:
        activity_schema["activity_type"].remove(to_remove)
    to_remove = None
    for index, validator in enumerate(activity_schema["object_id"]):
        if validator.__name__ == "object_id_validator":
            to_remove = validator
            break
    if to_remove:
        activity_schema["object_id"].remove(to_remove)
    activity_schema["object_id"].append(toolkit.get_validator("package_id_exists"))
    dataset = toolkit.get_action("package_show")(data_dict={"id": dataset_id})
    return toolkit.get_action("activity_create")(
        context={
            "ignore_auth": True,
            "schema": activity_schema,
        },
        data_dict={
            "user_id": toolkit.g.userobj.id,
            "object_id": dataset_id,
            "activity_type": activity_type.value,
            "data": {
                "package": dataset,
            },
        },
    )
