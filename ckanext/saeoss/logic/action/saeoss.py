import logging
import os
import pkg_resources
import typing

import ckan.plugins.toolkit as toolkit
import sqlalchemy

from ... import jobs

logger = logging.getLogger(__name__)


@toolkit.side_effect_free
def show_version(
        context: typing.Optional[typing.Dict] = None,
        data_dict: typing.Optional[typing.Dict] = None,
) -> typing.Dict:
    """return the current version of this project"""
    return {
        "version": pkg_resources.require("ckanext-saeoss")[0].version,
        "git_sha": os.getenv("GIT_COMMIT"),
    }


@toolkit.side_effect_free
def list_featured_datasets(
        context: typing.Dict,
        data_dict: typing.Optional[typing.Dict] = None,
) -> typing.List:
    toolkit.check_access("authorize_list_featured_datasets", context, data_dict)
    data_ = data_dict.copy() if data_dict is not None else {}
    include_private = data_.get("include_private", False)
    limit = data_.get("limit", 10)
    offset = data_.get("offset", 0)
    model = context["model"]
    query = (
        sqlalchemy.select([model.package_table.c.name])
        .select_from(model.package_table.join(model.package_extra_table))
        .where(
            sqlalchemy.and_(
                model.package_extra_table.c.featured == "true",
                model.package_table.c.state == "active",
                model.package_table.c.private == include_private,
            )
        )
        .limit(limit)
        .offset(offset)
    )
    return [r for r in query.execute()]


def _ensure_user_is_notifiable(user_id: str, dataset_id):
    toolkit.get_action("user_patch")(
        data_dict={"id": user_id, "activity_streams_email_notifications": True}
    )
    try:
        toolkit.get_action("follow_dataset")(
            data_dict={"id": dataset_id},
        )
    except toolkit.ValidationError:
        pass  # user is already following the dataset
