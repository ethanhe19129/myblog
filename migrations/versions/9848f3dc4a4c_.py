"""empty message

Revision ID: 9848f3dc4a4c
Revises: e6958269525f
Create Date: 2019-04-13 11:57:58.968446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9848f3dc4a4c'
down_revision = 'e6958269525f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.ID'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('replymessage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['message.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.ID'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('replymessage')
    op.drop_table('message')
    # ### end Alembic commands ###
