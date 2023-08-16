# define a table and a class to hold saved searches
# the class has a get method that returns a list of dcpr requets
# therree is also a mapper to map relationships


import datetime

from logging import getLogger

log = getLogger(__name__)

from sqlalchemy import orm, types, Column, Table, ForeignKey

from ckan import model


reporting_tool_table = Table(
    "reporting_tool",
    model.meta.metadata,
    Column(
        "reporting_tool_id",
        types.UnicodeText,
        primary_key=True,
        default=model.types.make_uuid,
    ),
    Column(
        "owner_user",
        types.UnicodeText,
        ForeignKey("user.id"),
        nullable=False,
    ),
    Column(
        "search_query",
        types.UnicodeText,
    ),
    Column(
        "search_type",
        types.UnicodeText,
    ),
    Column("search_date", types.DateTime, default=datetime.datetime.utcnow),
)


class ReportingTool(model.core.StatefulObjectMixin, model.domain_object.DomainObject):
    def __init__(self, **kw):
        super(ReportingTool, self).__init__(**kw)
        self.owner_id = kw.get("owner_user")

    def get(cls, **kw):
        """
        returns a list of saved searches
        based on user id.
        """
        query = model.meta.Session.query(cls)
        return query.filter_by(**kw)


model.meta.mapper(
    ReportingTool,
    reporting_tool_table,
    properties={
        "owner": orm.relationship(
            model.User,
            backref="reporting_tool",
            foreign_keys=reporting_tool_table.c.owner_user,
        ),
    },
)
