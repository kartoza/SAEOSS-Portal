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
from ckan.common import _, config, g, request


log = logging.getLogger(__name__)

from ckan.views import user

from ckan.common import _, c

from flask import Blueprint, request

log = logging.getLogger(__name__)
new_user_form = u'user/new_user_form.html'
edit_user_form = u'user/edit_user_form.html'

abort = base.abort
render = base.render

check_access = logic.check_access
get_action = logic.get_action
NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
UsernamePasswordError = logic.UsernamePasswordError

DataError = dictization_functions.DataError
unflatten = dictization_functions.unflatten

reset_password_blueprint = Blueprint(
    "password", __name__, url_prefix="/password"
)

def _lowercase(obj):
    """ Make dictionary lowercase """
    if isinstance(obj, dict):
        return {k.lower():_lowercase(v) for k, v in obj.items()}
    elif isinstance(obj, (list, set, tuple)):
        t = type(obj)
        return t(_lowercase(o) for o in obj)
    elif isinstance(obj, str):
        return obj.lower()
    else:
        return obj

class RequestResetPasswordView(MethodView):
    def _prepare(self):
        context = {
            u'model': model,
            u'session': model.Session,
            u'user': g.user,
            u'auth_user_obj': g.userobj
        }
        try:
            logic.check_access(u'request_reset', context)
        except logic.NotAuthorized:
            base.abort(403, _(u'Unauthorized to request reset password.'))

    def post(self):
        self._prepare()
        id = request.form.get(u'user')
        if id in (None, u''):
            h.flash_error(_(u'Email is required'))
            return h.redirect_to(u'/user/reset')
        # log.info(u'Password reset requested for user %s', repr_untrusted(id))

        context = {u'model': model, u'user': g.user, u'ignore_auth': True}
        user_objs = []

        # Usernames cannot contain '@' symbols
        if u'@' in id:
            # Search by email address
            # (You can forget a user id, but you don't tend to forget your
            # email)
            user_list = logic.get_action(u'user_list')(context, {
                u'email': id
            })
            if user_list:
                # send reset emails for *all* user accounts with this email
                # (otherwise we'd have to silently fail - we can't tell the
                # user, as that would reveal the existence of accounts with
                # this email address)
                for user_dict in user_list:
                    # type_ignore_reason: `user_list` returned the users,
                    #                     so we know they exist here.
                    user_objs.append(
                        model.User.get(user_dict['id']))  # type: ignore

        else:
            # Search by user name
            # (this is helpful as an option for a user who has multiple
            # accounts with the same email address and they want to be
            # specific)
            user_obj = model.User.get(id)
            if user_obj:
                user_objs.append(user_obj)

        # if not user_objs:
            # log.info(u'User requested reset link for unknown user: %s',
            #          repr_untrusted(id))

        for user_obj in user_objs:
            log.info(u'Emailing reset link to user: {}'
                     .format(user_obj.name))
            try:
                # FIXME: How about passing user.id instead? Mailer already
                # uses model and it allow to simplify code above
                mailer.send_reset_link(user_obj)
            except mailer.MailerException as e:
                # SMTP is not configured correctly or the server is
                # temporarily unavailable
                h.flash_error(_(u'Error sending the email. Try again later '
                                'or contact an administrator for help'))
                log.exception(e)
                return h.redirect_to(u'/password/reset')

        # commit any final changes and remove session
        model.repo.commit_and_remove()

        # always tell the user it succeeded, because otherwise we reveal
        # which accounts exist or not
        h.flash_success(
            _(u'A reset link has been emailed to you '
              '(unless the account specified does not exist)'))
        return h.redirect_to(u'/password/reset')

    def get(self):
        self._prepare()
        return base.render(u'user/request_reset.html', {})

    
reset_password_blueprint.add_url_rule(
    u'/reset', view_func=RequestResetPasswordView.as_view(str(u'request_reset')))
