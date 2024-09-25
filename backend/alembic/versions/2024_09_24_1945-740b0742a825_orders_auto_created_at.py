"""orders auto created at

Revision ID: 740b0742a825
Revises: 712d175ef5c2
Create Date: 2024-09-24 19:45:50.794151

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "740b0742a825"
down_revision: Union[str, None] = "712d175ef5c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "orders",
        "created_at",
        existing_type=sa.DATETIME(),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "orders",
        "created_at",
        existing_type=sa.DATETIME(),
        server_default=None,
        existing_nullable=False,
    )
    # ### end Alembic commands ###
