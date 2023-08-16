"""Added reporting tools table

Revision ID: cf3438c769b2
Revises: fbd4fb40d15c
Create Date: 2023-08-16 10:29:12.480609

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm, types, Table, ForeignKey
import datetime
from ckan import model

# revision identifiers, used by Alembic.
revision = 'cf3438c769b2'
down_revision = 'fbd4fb40d15c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "reporting_tool",
        model.meta.metadata,
        sa.Column(
            "reporting_tool_id",
            types.UnicodeText,
            primary_key=True,
            default=model.types.make_uuid,
        ),
        sa.Column(
            "owner_user",
            types.UnicodeText,
            ForeignKey("user.id"),
            nullable=False,
        ),
        sa.Column(
            "search_query",
            types.UnicodeText,
        ),
        sa.Column(
            "search_type",
            types.UnicodeText,
        ),
        sa.Column(
            "search_date", types.DateTime, default=datetime.datetime.utcnow
        ),
    )


def downgrade():
    op.drop_table("reporting_tool")