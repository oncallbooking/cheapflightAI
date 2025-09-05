"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('routes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('origin', sa.String(length=8), nullable=False),
        sa.Column('destination', sa.String(length=8), nullable=False),
        sa.Column('depart_date', sa.Date, nullable=True),
        sa.Column('return_date', sa.Date, nullable=True),
        sa.Column('cabin', sa.String(length=16), nullable=False, server_default='economy'),
        sa.Column('flex_days', sa.Integer, nullable=False, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('now()'), nullable=False)
    )
    op.create_table('sources',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=128), nullable=False, unique=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='active'),
        sa.Column('last_latency_ms', sa.Integer, nullable=True),
        sa.Column('error_rate', sa.Float, nullable=True),
        sa.Column('last_checked', sa.TIMESTAMP, nullable=True)
    )
    op.create_table('raw_flights',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('search_params', sa.JSON, nullable=False),
        sa.Column('scraped_at', sa.TIMESTAMP, nullable=False),
        sa.Column('source', sa.String(length=128), nullable=False),
        sa.Column('raw_payload', sa.JSON, nullable=True)
    )
    op.create_table('normalized_flights',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('raw_id', sa.BigInteger, sa.ForeignKey('raw_flights.id'), nullable=False),
        sa.Column('origin', sa.String(length=8), nullable=False),
        sa.Column('destination', sa.String(length=8), nullable=False),
        sa.Column('depart_date', sa.Date, nullable=True),
        sa.Column('return_date', sa.Date, nullable=True),
        sa.Column('airline', sa.String(length=64), nullable=True),
        sa.Column('flight_numbers', sa.JSON, nullable=True),
        sa.Column('departure_time', sa.TIMESTAMP, nullable=True),
        sa.Column('arrival_time', sa.TIMESTAMP, nullable=True),
        sa.Column('duration_minutes', sa.Integer, nullable=True),
        sa.Column('stops', sa.Integer, nullable=True),
        sa.Column('price_inr', sa.Float, nullable=False),
        sa.Column('booking_url', sa.String(length=1024), nullable=True),
        sa.Column('scraped_at', sa.TIMESTAMP, nullable=False)
    )
    op.create_table('deals',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('normalized_id', sa.BigInteger, sa.ForeignKey('normalized_flights.id'), nullable=False),
        sa.Column('score', sa.Float, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('now()'), nullable=False)
    )
    op.create_table('price_history',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('route_key', sa.String(length=64), nullable=False),
        sa.Column('date', sa.Date, nullable=True),
        sa.Column('cabins', sa.JSON, nullable=True),
        sa.Column('median_price_inr', sa.Float, nullable=True),
        sa.Column('recorded_at', sa.TIMESTAMP, server_default=sa.text('now()'), nullable=False)
    )
    op.create_index('ix_normalized_route_date_cabin', 'normalized_flights', ['origin', 'destination', 'depart_date'])

def downgrade():
    op.drop_index('ix_normalized_route_date_cabin', table_name='normalized_flights')
    op.drop_table('price_history')
    op.drop_table('deals')
    op.drop_table('normalized_flights')
    op.drop_table('raw_flights')
    op.drop_table('sources')
    op.drop_table('routes')
