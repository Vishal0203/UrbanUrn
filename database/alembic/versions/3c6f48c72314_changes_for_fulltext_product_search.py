"""changes for fulltext product search

Revision ID: 3c6f48c72314
Revises: 167a46ea121
Create Date: 2015-10-27 22:59:53.090000

"""

# revision identifiers, used by Alembic.
revision = '3c6f48c72314'
down_revision = '167a46ea121'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

alter_command_products_upgrade = """
ALTER TABLE products ADD COLUMN tsv tsvector;

CREATE TRIGGER products_tsvupdate BEFORE INSERT OR UPDATE ON products
FOR
each ROW EXECUTE PROCEDURE tsvector_update_trigger (tsv, 'pg_catalog.english', name, description);

CREATE INDEX products_fts_idx ON products USING gin(tsv);
"""


fts_changes_revert = """
ALTER TABLE products DROP COLUMN tsv;

DROP TRIGGER products_tsvupdate ON products;
"""


def upgrade():
    op.execute(alter_command_products_upgrade)
    pass


def downgrade():
    op.execute(fts_changes_revert)
    pass
