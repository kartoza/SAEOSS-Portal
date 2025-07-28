"""Add sitewide user permissions table

Revision ID: 25305b672285
Revises: 796cac900039
Create Date: 2025-07-21 10:18:16.253621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25305b672285'
down_revision = '796cac900039'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sitewide_admin_permission',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Unicode(), sa.ForeignKey('user.id'), nullable=False),  # changed from Integer to Unicode
        sa.Column('permission', sa.Unicode(), nullable=False),
        sa.Column('can_edit', sa.Boolean(), default=False),
        sa.Column('can_view', sa.Boolean(), default=True),
        sa.Column('created', sa.DateTime(), server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('sitewide_admin_permission')
