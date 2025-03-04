"""alter_tenant_table

Revision ID: 0bc1ff9ed013
Revises: 639849ef95e4
Create Date: 2025-03-05 00:44:10.189194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0bc1ff9ed013'
down_revision: Union[str, None] = '639849ef95e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tenants', sa.Column('company_country', sa.String(length=255), nullable=True))
    op.add_column('tenants', sa.Column('industry', sa.String(length=255), nullable=True))
    op.add_column('tenants', sa.Column('workspace_name', sa.String(length=255), nullable=True))
    op.add_column('tenants', sa.Column('account_owner_handle', sa.Text(), nullable=True))
    op.add_column('tenants', sa.Column('solutions_interested', sa.Text(), nullable=True))
    op.drop_column('tenants', 'industry_type')
    op.drop_column('tenants', 'otp')
    op.drop_column('tenants', 'otp_expiry_at')
    op.add_column('users', sa.Column('otp', sa.String(length=6), nullable=True))
    op.add_column('users', sa.Column('otp_expiry_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'otp_expiry_at')
    op.drop_column('users', 'otp')
    op.add_column('tenants', sa.Column('otp_expiry_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('tenants', sa.Column('otp', sa.VARCHAR(length=6), autoincrement=False, nullable=True))
    op.add_column('tenants', sa.Column('industry_type', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('tenants', 'solutions_interested')
    op.drop_column('tenants', 'account_owner_handle')
    op.drop_column('tenants', 'workspace_name')
    op.drop_column('tenants', 'industry')
    op.drop_column('tenants', 'company_country')
    # ### end Alembic commands ###
