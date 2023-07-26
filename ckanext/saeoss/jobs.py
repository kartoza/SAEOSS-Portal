# -*- coding: utf-8 -*-

"""Asynchronous jobs for SAEOSS portal."""

import logging
import typing

from ckan import model
from ckan.plugins import toolkit

from . import (
    email_notifications,
)
from .constants import (
    DatasetManagementActivityType,
)

logger = logging.getLogger(__name__)


def test_job(*args, **kwargs):
    logger.debug(f"inside test_job - {args=} {kwargs=}")


def notify_org_admins_of_dataset_management_request(activity_id: str):
    """Send a request of management to an organisation admin

    :param
    activity_id: The activity to request
    :type
    activity_id: str
    """
    activity_obj = model.Activity.get(activity_id)
    if activity_obj is not None:
        activity_type = DatasetManagementActivityType(activity_obj.activity_type)
        dataset = (activity_obj.data or {}).get("package")
        templates_map = {
            DatasetManagementActivityType.REQUEST_PUBLICATION: (),
            DatasetManagementActivityType.REQUEST_MAINTENANCE: (
                "email_notifications/dataset_maintenance_request_subject.txt",
                "email_notifications/dataset_maintenance_request_body.txt",
            ),
        }
        if dataset is not None:
            org_id = dataset["owner_org"]
            organization = toolkit.get_action("organization_show")(
                context={"ignore_auth": True},
                data_dict={
                    "id": org_id,
                    "include_users": True,
                },
            )
            jinja_env = email_notifications.get_jinja_env()
            subject_path, body_path = templates_map[activity_type]
            subject_template = jinja_env.get_template(subject_path)
            body_template = jinja_env.get_template(body_path)
            for member in organization.get("users", []):
                is_active = member.get("state") == "active"
                is_org_admin = member.get("capacity") == "admin"
                if is_active and is_org_admin:
                    user_obj = model.User.get(member["id"])
                    logger.debug(
                        f"About to send a notification to {user_obj.name!r}..."
                    )
                    subject = subject_template.render(
                        site_title=toolkit.config.get("ckan.site_title", "SASDI EMC")
                    )
                    body = body_template.render(
                        organization=organization,
                        user_obj=user_obj,
                        dataset=dataset,
                        h=toolkit.h,
                        site_url=toolkit.config.get("ckan.site_url", ""),
                    )
                    email_notifications.send_notification(
                        {
                            "name": user_obj.name,
                            "display_name": user_obj.display_name,
                            "email": user_obj.email,
                        },
                        {"subject": subject, "body": body},
                    )
    else:
        raise RuntimeError(f"Could not retrieve activity with id {activity_id!r}")
    

def _get_org_members(org_name: str) -> typing.List:
    """Get all organisation members.

    :param
    org_name: The name the organisation
    :type
    org_name:str

    """
    organization: typing.Dict = toolkit.get_action("organization_show")(
        context={"ignore_auth": True},
        data_dict={
            "id": org_name,
            "include_users": True,
        },
    )
    members = []
    for user in organization.get("users", []):
        user_obj = model.User.get(user["id"])
        if user.get("state") == "active":
            members.append(user_obj)
    return members
