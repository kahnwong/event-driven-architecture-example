"""rename to transcript

Revision ID: 399c1bf6ebeb
Revises: 5348111d5bca
Create Date: 2024-08-13 17:42:08.659849

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '399c1bf6ebeb'
down_revision = '5348111d5bca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('foo', sa.Column('transcript', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.drop_column('foo', 'transcription')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('foo', sa.Column('transcription', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('foo', 'transcript')
    # ### end Alembic commands ###