# -*- coding: utf-8 -*-
"""Override of CKAN actions"""
import json
import logging
import typing

import ckan.plugins.toolkit as toolkit
from ckan.logic.action.get import package_show as _package_show
from ckan.model.domain_object import DomainObject
import ckan.logic as logic
from .add_named_url import populate_dataset_name, sanitize_title
from ...model.user_extra_fields import UserExtraFields
from ckanext.saeoss.helpers import _get_reference_date, _get_tags
from mimetypes import MimeTypes
from ...helpers import sanitize_tag

logger = logging.getLogger(__name__)
ValidationError = logic.ValidationError

mimeNotAllowed = [
    "text/html", 
    "application/java", 
    "application/java-byte-code", 
    "application/x-javascript", 
    "application/javascript", 
    "application/ecmascript", 
    "text/javascript", 
    "text/ecmascript",
    "application/octet-stream",
    "text/x-server-parsed-html",
    "text/x-server-parsed-html"
]

@toolkit.chained_action
def user_show(original_action, context, data_dict):
    """
    Intercepts the core `user_show` action to add any extra_fields that may exist for
    the user
    """

    original_result = original_action(context, data_dict)
    user_id = original_result.get("id")
    model = context["model"]
    user_obj = model.Session.query(model.User).filter_by(id=user_id).first()
    if user_obj.extra_fields is not None:
        original_result["extra_fields"] = _dictize_user_extra_fields(
            user_obj.extra_fields
        )
    else:
        original_result["extra_fields"] = None
    return original_result


@toolkit.chained_action
def user_update(original_action, context, data_dict):
    """
    Intercepts the core `user_update` action to update any extra_fields that may exist
    for the user. Also checks if the user is updating their image before validating MIME type.
    """
    original_result = original_action(context, data_dict)
    
    # Check if image_url is being updated
    if "image_url" in data_dict and data_dict["image_url"]:
        mime = MimeTypes()
        mime_type = mime.guess_type(data_dict["image_url"])
        
        if mime_type[0] in mimeNotAllowed:
            raise ValidationError([f"Mimetype {mime_type[0]} is not allowed!"])
    
    user_id = original_result["id"]
    model = context["model"]
    user_obj = model.Session.query(model.User).filter_by(id=user_id).first()
    
    if user_obj.extra_fields is None:
        extra = UserExtraFields(user_id=user_id)
    else:
        extra = user_obj.extra_fields
    
    extra.affiliation = data_dict.get("extra_fields_affiliation")
    extra.professional_occupation = data_dict.get("extra_fields_professional_occupation")
    
    model.Session.add(extra)
    model.Session.commit()
    
    original_result["extra_fields"] = _dictize_user_extra_fields(extra)
    return original_result



@toolkit.chained_action
def user_create(original_action, context, data_dict):
    """Intercepts the core `user_create` action to also create the extra_fields."""
    original_result = original_action(context, data_dict)
    user_id = original_result["id"]
    model = context["model"]
    extra = UserExtraFields(
        user_id=user_id,
        affiliation=data_dict.get("extra_fields") or "",
        professional_occupation=data_dict.get("extra_fields") or "",
    )
    model.Session.add(extra)
    model.Session.commit()
    original_result["extra_fields"] = _dictize_user_extra_fields(extra)
    return original_result

@toolkit.chained_action
def organization_update(original_action, context, data_dict):
    original_result = original_action(context, data_dict)
    mime = MimeTypes()
    mime_type = mime.guess_type(original_result["image_url"])
    
    if mime_type[0] in mimeNotAllowed:
        raise ValidationError([f"Mimetype {mime_type} is not allowed!"])
    return original_result


def _dictize_user_extra_fields(user_extra_fields: UserExtraFields) -> typing.Dict:
    dictized_extra = DomainObject.as_dict(user_extra_fields)
    del dictized_extra["id"]
    del dictized_extra["user_id"]
    return dictized_extra


@toolkit.chained_action
def package_show(original_action, context, data_dict):
    """
    Intercepts the core `package_show` action to add reference_date to package dict
    """
    package_dict = _package_show(context, data_dict)
    package_dict['reference_date'] = _get_reference_date(package_dict)
    return package_dict


@toolkit.chained_action
def package_create(original_action, context, data_dict):
    data_dict["name"] = sanitize_title(data_dict.get("title"))

    tag_controlled = data_dict.get("tag_controlled_string")

    if isinstance(tag_controlled, str):
        tag_controlled = [tag_controlled]

    if tag_controlled:
        cleaned_tags = [sanitize_tag(tag.strip()) for tag in tag_controlled if tag.strip()]
        data_dict["tags"] = [{"name": tag} for tag in cleaned_tags]
        data_dict["tag_string"] = ','.join(cleaned_tags)

    return _act_depending_on_package_visibility(original_action, context, data_dict)



@toolkit.chained_action
def package_update(original_action, context, data_dict):
    """
    Intercepts the core `package_update` action to check if package is being published.
    """
    tag_controlled = data_dict.get("tag_controlled_string")

    if isinstance(tag_controlled, str):
        tag_controlled = [tag_controlled]

    if tag_controlled:
        cleaned_tags = [sanitize_tag(tag.strip()) for tag in tag_controlled if tag.strip()]
        data_dict["tags"] = [{"name": tag} for tag in cleaned_tags]
    
    try:
        data_dict['tags'] = _get_tags(data_dict)
    except KeyError:
        data_dict['tags'] = []
    
    data_dict['tag_string'] = ','.join([tag['name'] for tag in data_dict['tags']])
    return _act_depending_on_package_visibility(original_action, context, data_dict)


@toolkit.chained_action
def package_patch(original_action, context, data_dict):
    """
    Intercepts the core `package_patch` action to check if package is being published.
    """
    return _act_depending_on_package_visibility(original_action, context, data_dict)


def user_patch(context: typing.Dict, data_dict: typing.Dict) -> typing.Dict:
    """Implements user_patch action, which is not available on CKAN

    The `data_dict` parameter is expected to contain at least the `id` key, which
    should hold the user's id or name

    """

    logger.debug("About to check access of user_update")
    toolkit.check_access("user_update", context, data_dict)
    show_context = {
        "model": context["model"],
        "session": context["session"],
        "user": context["user"],
        "auth_user_obj": context["auth_user_obj"],
    }
    user_dict = toolkit.get_action("user_show")(
        show_context, data_dict={"id": context["user"]}
    )
    patched = dict(user_dict)
    patched.update(data_dict)
    update_action = toolkit.get_action("user_update")
    return update_action(context, patched)


def _act_depending_on_package_visibility(
    action: typing.Callable, context: typing.Dict, data: typing.Dict
):
    remains_private = toolkit.asbool(data.get("private", True))
    if remains_private:
        result = action(context, data)
    else:
        access = toolkit.check_access("package_publish", context, data)
        result = action(context, data) if access else None
        # if you create, update or patch you are following the dataset
        # this make a failure when the dataset is changed from private to public:
        # message form contains invalid entries: Y (maybe because the user already follow ? )
        # if access:
        #     toolkit.get_action("follow_dataset")(context, result)

    return result
