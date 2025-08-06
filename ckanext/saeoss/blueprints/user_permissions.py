# encoding: utf-8
import logging

from flask import Blueprint
from flask.views import MethodView
from ckan.common import asbool
from six import text_type, ensure_str
import dominate.tags as dom_tags

import ckan.lib.authenticator as authenticator
import ckan.lib.base as base
import ckan.lib.captcha as captcha
import ckan.lib.helpers as h
import ckan.lib.mailer as mailer
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.logic as logic
import ckan.logic.schema as schema
import ckan.model as model
import ckan.plugins as plugins
from ckan import authz
from ckan.common import _, config, g, request, repr_untrusted
from ckan.views.user import user

from ..model.user_permissions import SitewideAdminPermission, sitewide_admin_permissions_table

log = logging.getLogger(__name__)

user_permission_blueprint = Blueprint(
    "permissions", __name__, template_folder="templates", url_prefix="/permissions"
)


user_permissions = u'user/user_permissions.html'

class PermissionView(MethodView):
    def _prepare(self, id):
        context = {
            u'save': u'save' in request.form,
            u'schema': _edit_form_to_db_schema(),
            u'model': model,
            u'session': model.Session,
            u'user': g.user,
            u'auth_user_obj': g.userobj
        }
        if id is None:
            if g.userobj:
                id = g.userobj.id
            else:
                base.abort(400, _(u'No user specified'))
        data_dict = {u'id': id}

        try:
            logic.check_access(u'user_update', context, data_dict)
        except logic.NotAuthorized:
            base.abort(403, _(u'Unauthorized to edit a user.'))
        return context, id

    def post(self, id=None):
        context, id = self._prepare(id)
        if not context[u'save']:
            return self.get(id)

        session = model.Session

        try:
            data_dict = logic.clean_dict(
                dictization_functions.unflatten(
                    logic.tuplize_dict(logic.parse_params(request.form))))
            data_dict.update(logic.clean_dict(
                dictization_functions.unflatten(
                    logic.tuplize_dict(logic.parse_params(request.files))))
            )
        except dictization_functions.DataError:
            base.abort(400, _(u'Integrity Error'))

        # Fetch user by username
        user = model.User.by_name(id)
        if not user:
            base.abort(404, _(u'User not found'))

        # Extract form values
        permission_name = 'allow_create_orgs'
        can_edit = data_dict.get(u'allow_create_orgs', False)
        can_view = data_dict.get(u'allow_create_orgs', True)

        # Convert to booleans
        can_edit = asbool(can_edit)
        can_view = asbool(can_view)

        # Check if permission already exists
        existing = session.query(SitewideAdminPermission).filter_by(
            user_id=user.id, permission=permission_name).first()

        if existing:
            existing.can_edit = can_edit
            existing.can_view = can_view
        else:
            new_perm = SitewideAdminPermission(
                user_id=user.id,
                permission=permission_name,
                can_edit=can_edit,
                can_view=can_view
            )
            session.add(new_perm)

        try:
            session.commit()
            h.flash_success(_(u'Permission updated'))
        except Exception as e:
            session.rollback()
            base.abort(500, _(u'Failed to save permission: {}').format(str(e)))

        return h.redirect_to(u'permissions.edit', id=user.name)

    def get(self, id=None, data=None, errors=None, error_summary=None):
        context, id = self._prepare(id)
        data_dict = {u'id': id}

        try:
            old_data = logic.get_action(u'user_show')(context, data_dict)

            g.display_name = old_data.get(u'display_name')
            g.user_name = old_data.get(u'name')

            data = data or old_data

            # Fetch user's sitewide admin permissions
            user = model.User.by_name(id)
            if not user:
                base.abort(404, _(u'User not found'))

            permissions = model.Session.query(SitewideAdminPermission).filter_by(user_id=user.id).all()

            # Add the permissions list under 'allow_create_orgs'
            data[u'allow_create_orgs'] = [
                {
                    'permission': p.permission,
                    'can_edit': p.can_edit,
                    'can_view': p.can_view
                }
                for p in permissions
            ]

        except logic.NotAuthorized:
            base.abort(403, _(u'Unauthorized to edit user %s') % u'')
        except logic.NotFound:
            base.abort(404, _(u'User not found'))

        errors = errors or {}
        vars = {
            u'data': data,
            u'errors': errors,
            u'error_summary': error_summary
        }

        extra_vars = _extra_template_variables({
            u'model': model,
            u'session': model.Session,
            u'user': g.user
        }, data_dict)

        extra_vars[u'show_email_notifications'] = asbool(
            config.get(u'ckan.activity_streams_email_notifications'))
        vars.update(extra_vars)
        extra_vars[u'form'] = base.render(user_permissions, extra_vars=vars)

        return base.render(u'user/edit.html', extra_vars)
    

def _extra_template_variables(context, data_dict):
    is_sysadmin = authz.is_sysadmin(g.user)
    try:
        user_dict = logic.get_action(u'user_show')(context, data_dict)
    except logic.NotFound:
        base.abort(404, _(u'User not found'))
    except logic.NotAuthorized:
        base.abort(403, _(u'Not authorized to see this page'))

    is_myself = user_dict[u'name'] == g.user
    about_formatted = h.render_markdown(user_dict[u'about'])
    extra = {
        u'is_sysadmin': is_sysadmin,
        u'user_dict': user_dict,
        u'is_myself': is_myself,
        u'about_formatted': about_formatted
    }
    return extra

def set_repoze_user(user_id, resp):
    u'''Set the repoze.who cookie to match a given user_id'''
    if u'repoze.who.plugins' in request.environ:
        rememberer = request.environ[u'repoze.who.plugins'][u'friendlyform']
        identity = {u'repoze.who.userid': user_id}
        resp.headers.extend(rememberer.remember(request.environ, identity))

def _edit_form_to_db_schema():
    return schema.user_edit_form_schema()

_edit_view = PermissionView.as_view(str(u'edit'))
user_permission_blueprint.add_url_rule(u'/edit', view_func=_edit_view)
user_permission_blueprint.add_url_rule(u'/edit/<id>/', view_func=_edit_view)