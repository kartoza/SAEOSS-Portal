"""Add stac harvest table

Revision ID: 796cac900039
Revises: cf3438c769b2
Create Date: 2023-10-11 11:37:26.280343

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm, types, Table, ForeignKey
import datetime
from ckan import model

# revision identifiers, used by Alembic.
revision = '796cac900039'
down_revision = 'cf3438c769b2'
branch_labels = None
depends_on = None


def upgrade():
    """Create table function."""
    op.create_table(
        "stac_harvester",
        model.meta.metadata,
        sa.Column(
            "harvester_id",
            types.UnicodeText,
            primary_key=True,
            default=model.types.make_uuid,
        ),
        sa.Column(
            "user",
            types.UnicodeText,
        ),
        sa.Column(
            "owner_org",
            types.UnicodeText,
        ),
        sa.Column(
            "url",
            types.UnicodeText,
        ),
        sa.Column(
            "number_records",
            types.UnicodeText,
        ),
        sa.Column(
            "status",
            types.UnicodeText,
        ),
        sa.Column(
            "message",
            types.UnicodeText,
        ),
        sa.Column(
            "_date", types.DateTime, default=datetime.datetime.utcnow
        ),
    )


def downgrade():
    """To delete table function."""
    op.drop_table("stac_harvester")
