"""Initial revision

Revision ID: 168ee7e8f406
Revises: 
Create Date: 2022-03-15 16:14:15.472993

"""
from alembic import op
import sqlalchemy as sa
from data.hash import Hash


# revision identifiers, used by Alembic.
revision = '168ee7e8f406'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    users_table = op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.Text(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)
    op.create_table('trips',
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('completeness', sa.Boolean(), nullable=True),
    sa.Column('contact', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('trip_id')
    )
    op.create_index(op.f('ix_trips_trip_id'), 'trips', ['trip_id'], unique=False)
    # ### end Alembic commands ###

    op.bulk_insert(
        users_table,
        [
            {"name": "admin",
             "email": "noone@blablabla",
             "password": Hash.get_password_hash("admin"),
             "is_active": True,
             "is_admin": True}
        ]
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_trips_trip_id'), table_name='trips')
    op.drop_table('trips')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
