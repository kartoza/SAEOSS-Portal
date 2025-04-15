import enum
import logging
import typing

import re
import click
from ckan import model
from ckan.logic import NotFound
from ckan.lib import jinja_extensions
from ckan.plugins import toolkit
from flask_babel import gettext as flask_ugettext, ngettext as flask_ungettext
from jinja2 import Environment

logger = logging.getLogger(__name__)


class DatasetCreationResult(enum.Enum):
    CREATED = "created"
    NOT_CREATED_ALREADY_EXISTS = "already_exists"
    UPDATED = "updated"
    FAILED_VALIDATION = "failed_validation"


def get_jinja_env():
    jinja_env = Environment(**jinja_extensions.get_jinja_env_options())
    jinja_env.install_gettext_callables(flask_ugettext, flask_ungettext, newstyle=True)
    # custom filters
    jinja_env.policies["ext.i18n.trimmed"] = True
    jinja_env.filters["empty_and_escape"] = jinja_extensions.empty_and_escape
    # jinja_env.filters["ungettext"] = flask_ungettext
    return jinja_env


def sanitize_dataset_name(name: str) -> str:
    """
    Converts a string to a CKAN-compliant dataset name.
    """
    # Lowercase, replace spaces with dashes, remove invalid characters
    name = name.lower().replace(" ", "-")
    name = re.sub(r"[^a-z0-9\-_]", "", name)
    return name


def create_single_dataset(
    user: typing.Dict, dataset: typing.Dict, close_session: bool = False
) -> DatasetCreationResult:
    dataset = dataset.copy()
    dataset["name"] = sanitize_dataset_name(dataset["name"])

    context = {"user": user["name"]}

    try:
        existing = toolkit.get_action("package_show")(context, data_dict={"id": dataset["name"]})
        dataset["id"] = existing["id"]
        toolkit.get_action("package_update")(context, data_dict=dataset)
        result = DatasetCreationResult.UPDATED
        logger.debug(f"Dataset {dataset['name']!r} updated.")
    except toolkit.ObjectNotFound:
        toolkit.get_action("package_create")(context, data_dict=dataset)
        result = DatasetCreationResult.CREATED
        logger.debug(f"Dataset {dataset['name']!r} created.")
    except toolkit.ValidationError as e:
        logger.error(f"Validation error for dataset {dataset['name']!r}: {e.error_dict}")
        result = DatasetCreationResult.FAILED_VALIDATION

    if close_session:
        model.Session.remove()
      
    return result


def create_org_user(
    user_id: str,
    user_password: str,
    *,
    organization_memberships: typing.List[typing.Dict[str, str]],
    user_email: typing.Optional[str] = None,
) -> typing.Dict:
    creator = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    user_details = toolkit.get_action("user_create")(
        context={
            "user": creator["name"],
        },
        data_dict={
            "name": user_id,
            "email": user_email or f"{user_id}@dummy.mail",
            "password": user_password,
        },
    )
    for membership in organization_memberships:
        org_details = toolkit.get_action("organization_show")(
            data_dict={"id": membership["org_id"]}
        )
        member_details = toolkit.get_action("organization_member_create")(
            context={
                "user": creator["name"],
            },
            data_dict={
                "id": org_details.name,
                "username": user_id,
                "role": membership["role"],
            },
        )
    return user_details


def maybe_create_organization(
    name: str,
    title: typing.Optional[str] = None,
    description: typing.Optional[str] = None,
    close_session: bool = False,
) -> typing.Tuple[typing.Dict, bool]:
    try:
        organization = toolkit.get_action("organization_show")(
            data_dict={
                "id": name,
                "include_users": True,
                "include_datasets": False,
                "include_dataset_count": False,
                "include_groups": False,
                "include_tags": False,
                "include_followers": False,
            }
        )
        created = False
    except NotFound:  # org does not exist yet, create it
        user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
        data_dict = {
            "name": name,
            "title": title,
            "description": description,
        }
        data_dict = {k: v for k, v in data_dict.items() if v is not None}
        organization = toolkit.get_action("organization_create")(
            context={"user": user["name"]},
            data_dict=data_dict,
        )
        created = True
    if close_session:
        model.Session.remove()
    return organization, created


class ClickLoggingHandler(logging.Handler):
    """Custom logging handler to allow using click output functions"""

    def emit(self, record: logging.LogRecord) -> None:
        fg = None
        bg = None
        if record.levelno == logging.DEBUG:
            fg = "black"
            bg = "bright_white"
        elif record.levelno == logging.INFO:
            fg = "bright_blue"
        elif record.levelno == logging.WARNING:
            fg = "bright_magenta"
        elif record.levelno == logging.CRITICAL:
            fg = "bright_red"
        elif record.levelno == logging.ERROR:
            fg = "bright_white"
            bg = "red"
        click.secho(self.format(record), bg=bg, fg=fg)
