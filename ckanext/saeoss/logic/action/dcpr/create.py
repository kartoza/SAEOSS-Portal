import logging

from ckan.plugins import toolkit
from sqlalchemy import exc

from .... import dcpr_dictization
from ...schema import create_dcpr_request_schema
from ....model import dcpr_request
from ....constants import (
    DcprManagementActivityType,
    DCPRRequestStatus,
)

logger = logging.getLogger(__name__)

def dcpr_request_create(context, data_dict):
    logger.debug(f"{data_dict=}")
    model = context["model"]
    schema = context.get("schema", create_dcpr_request_schema())
    logger.debug(f"{schema=}")
    validated_data, errors = toolkit.navl_validate(data_dict, schema, context)
    logger.debug(f"{errors=}")
    if errors:
        model.Session.rollback()
        raise toolkit.ValidationError(errors)

    # add validation error to capture_end_date
    date_start = data_dict["capture_start_date"]
    date_end = data_dict["capture_end_date"]
    if date_end < date_start:
        raise toolkit.ValidationError(
            {
                "capture_end_date": [
                    "Invalid value. Please select a date after capture start date."
                ],
            }
        )
    toolkit.check_access("dcpr_request_create_auth", context, validated_data)

    # after validation of user-supplied data, enrich the data dict with additional
    # required attributes, like the request owner, status, etc.
    validated_data.update(
        {
            "owner_user": context["auth_user_obj"].id,
            "status": DCPRRequestStatus.UNDER_PREPARATION.value,
        }
    )
    logger.debug(f"{validated_data=}")
    context["updated_by"] = "owner"
    request_obj = dcpr_dictization.dcpr_request_dict_save(validated_data, context)
    model.Session.commit()
    logger.debug(f"{request_obj=}")
    create_dcpr_management_activity(
        request_obj,
        activity_type=DcprManagementActivityType.CREATE_DCPR_REQUEST,
        context=context,
    )
    return toolkit.get_action("dcpr_request_show")(
        context=context.copy(),
        data_dict={"csi_reference_id": request_obj.csi_reference_id},
    )
