"""Update products table name length

Revision ID: 47fa5d3bc76
Revises: 50fa7b6b038
Create Date: 2015-12-26 17:21:49.669011

"""

# revision identifiers, used by Alembic.
revision = '47fa5d3bc76'
down_revision = '50fa7b6b038'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('ALTER TABLE products ALTER COLUMN name TYPE character varying(255)')


def downgrade():
    op.execute('ALTER TABLE products ALTER COLUMN name TYPE character varying(50)')
