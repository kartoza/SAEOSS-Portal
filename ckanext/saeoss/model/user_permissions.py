from sqlalchemy import Table, Column, Integer, Unicode, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import mapper, relationship
from ckan.model import meta, User

sitewide_admin_permissions_table = Table('sitewide_admin_permission', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('permission', Unicode, nullable=False),
    Column('can_edit', Boolean, default=False),
    Column('can_view', Boolean, default=True),
    Column('created', DateTime, default=func.now())
)

class SitewideAdminPermission(object):
    def __init__(self, user_id, permission, can_edit=False, can_view=True):
        self.user_id = user_id
        self.permission = permission
        self.can_edit = can_edit
        self.can_view = can_view

mapper(SitewideAdminPermission, sitewide_admin_permissions_table, properties={
    'user': relationship(User, backref='sitewide_permissions')
})
