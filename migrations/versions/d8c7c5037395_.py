"""empty message

Revision ID: d8c7c5037395
Revises: 52651d20698f
Create Date: 2019-04-11 11:38:16.866809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8c7c5037395'
down_revision = '52651d20698f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recommend',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reco_type', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('topic', sa.Column('recommend_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'topic', 'recommend', ['recommend_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'topic', type_='foreignkey')
    op.drop_column('topic', 'recommend_id')
    op.drop_table('recommend')
    # ### end Alembic commands ###