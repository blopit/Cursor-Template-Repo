"""Initial database schema migration

Revision ID: 001
Revises: None
Create Date: 2024-02-20
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# Revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table with proper timestamps and validation
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    )
    
    # Add indexes for performance
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    # Remove indexes first
    op.drop_index('idx_users_email')
    
    # Then remove tables
    op.drop_table('users') 