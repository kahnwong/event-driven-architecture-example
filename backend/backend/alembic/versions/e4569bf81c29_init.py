"""init

Revision ID: e4569bf81c29
Revises:
Create Date: 2024-08-13 13:51:12.923298

"""

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op


# revision identifiers, used by Alembic.
revision = "e4569bf81c29"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "foo",
        sa.Column("request_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("message", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("progress", sa.Integer(), nullable=False),
        sa.Column("is_done", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("request_id"),
    )
    op.create_index(op.f("ix_foo_request_id"), "foo", ["request_id"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_foo_request_id"), table_name="foo")
    op.drop_table("foo")
    # ### end Alembic commands ###
