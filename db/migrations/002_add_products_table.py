"""Add products table

Revision ID: 002
Revises: 001
Create Date: 2024-03-20
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# Revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Create products table with proper timestamps and validation
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    )
    
    # Add indexes for performance
    op.create_index('idx_products_name', 'products', ['name'])

def downgrade():
    # Remove indexes first
    op.drop_index('idx_products_name')
    
    # Then remove table
    op.drop_table('products') 