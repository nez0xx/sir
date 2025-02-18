"""empty message

Revision ID: d86fc3e6b73f
Revises: efdce543417c
Create Date: 2024-12-08 18:05:28.015392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd86fc3e6b73f'
down_revision: Union[str, None] = 'efdce543417c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('anonmessages', sa.Column('to_chat_id', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('anonmessages', 'to_chat_id')
    # ### end Alembic commands ###
