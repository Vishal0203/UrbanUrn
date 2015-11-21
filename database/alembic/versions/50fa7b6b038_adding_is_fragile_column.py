"""adding_is_fragile_column

Revision ID: 50fa7b6b038
Revises: 2e9ee3973bcc
Create Date: 2015-11-21 14:52:43.076618

"""

# revision identifiers, used by Alembic.
revision = '50fa7b6b038'
down_revision = '2e9ee3973bcc'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


upgrade_command = '''
ALTER TABLE products ADD COLUMN is_fragile boolean default false;
'''

downgrade_command = '''
ALTER TABLE products DROP COLUMN is_fragile;
'''


def upgrade():
    op.execute(upgrade_command)


def downgrade():
    op.execute(downgrade_command)
