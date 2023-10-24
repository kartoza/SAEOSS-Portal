# define a table and a class to hold saved searches
# the class has a get method that returns a list of dcpr requets
# therree is also a mapper to map relationships


import datetime

from logging import getLogger

log = getLogger(__name__)

from sqlalchemy import orm, types, Column, Table, ForeignKey

from ckan import model


stac_harvester_table = Table(
    "stac_harvester",
    model.meta.metadata,
    Column(
        "harvester_id",
        types.UnicodeText,
        primary_key=True,
        default=model.types.make_uuid,
    ),
    Column(
        "user",
        types.UnicodeText,
    ),
    Column(
        "owner_org",
        types.UnicodeText,
    ),
    Column(
        "url",
        types.UnicodeText,
    ),
    Column(
        "number_records",
        types.UnicodeText,
    ),
    # Column(
    #     "processed_records",
    #     types.Integer,
    # ),
    # Column(
    #     "created_records",
    #     types.Integer,
    # ),
    Column(
        "status",
        types.UnicodeText,
    ),
    Column(
        "message",
        types.UnicodeText,
    ),
    Column("_date", types.DateTime, default=datetime.datetime.utcnow),
)


class StacHarvester(model.core.StatefulObjectMixin, model.domain_object.DomainObject):
    def __init__(self, **kw):
        super(StacHarvester, self).__init__(**kw)
        self.owner_id = kw.get("user")

    def get(cls, **kw):
        """
        returns a list of saved searches
        based on user id.
        """
        query = model.meta.Session.query(cls)
        return query.filter_by(**kw)


model.meta.mapper(
    StacHarvester,
    stac_harvester_table,
    properties={
        "owner": orm.relationship(
            model.User,
            backref="stac_harvester",
        ),
    },
)
