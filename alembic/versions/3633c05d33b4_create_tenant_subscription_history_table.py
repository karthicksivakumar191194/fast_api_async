"""create tenant subscription history table

Revision ID: 3633c05d33b4
Revises: 0c36332ce06a
Create Date: 2025-02-25 14:48:38.579303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3633c05d33b4'
down_revision: Union[str, None] = '0c36332ce06a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tenant_subscription_history',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('tenant_id', sa.UUID(), nullable=False),
    sa.Column('subscription_plan', sa.UUID(), nullable=False),
    sa.Column('price_month_rupee', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('price_year_rupee', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('price_month_dollar', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('price_year_dollar', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('plan_type', sa.String(length=255), nullable=False),
    sa.Column('plan_price_type', sa.String(length=255), nullable=False),
    sa.Column('invoice_number', sa.Integer(), nullable=False),
    sa.Column('invoice_url', sa.String(length=255), nullable=True),
    sa.Column('start_timestamp', sa.DateTime(), nullable=True),
    sa.Column('end_timestamp', sa.DateTime(), nullable=True),
    sa.Column('payment_via', sa.String(length=255), nullable=False),
    sa.Column('expiry_days', sa.Integer(), nullable=True),
    sa.Column('expiry_date', sa.Date(), nullable=True),
    sa.Column('status', sa.Enum('DELETED', 'ACTIVE', 'IN_ACTIVE', name='subscriptionhistorystatusenum'), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['subscription_plan'], ['subscription_plans.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('invoice_number')
    )
    op.create_index('idx_org_sub_hist_expiry_date', 'tenant_subscription_history', ['expiry_date'], unique=False)
    op.create_index('idx_org_sub_hist_invoice_number', 'tenant_subscription_history', ['invoice_number'], unique=False)
    op.create_index('idx_org_sub_hist_payment_via', 'tenant_subscription_history', ['payment_via'], unique=False)
    op.create_index('idx_org_sub_hist_plan_price_type', 'tenant_subscription_history', ['plan_price_type'], unique=False)
    op.create_index('idx_org_sub_hist_plan_type', 'tenant_subscription_history', ['plan_type'], unique=False)
    op.create_index('idx_org_sub_hist_status', 'tenant_subscription_history', ['status'], unique=False)
    op.create_index('idx_org_sub_hist_subscription_plan', 'tenant_subscription_history', ['subscription_plan'], unique=False)
    op.create_index('idx_org_sub_hist_tenant_id', 'tenant_subscription_history', ['tenant_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_org_sub_hist_tenant_id', table_name='tenant_subscription_history')
    op.drop_index('idx_org_sub_hist_subscription_plan', table_name='tenant_subscription_history')
    op.drop_index('idx_org_sub_hist_status', table_name='tenant_subscription_history')
    op.drop_index('idx_org_sub_hist_plan_type', table_name='tenant_subscription_history')
    op.drop_index('idx_org_sub_hist_plan_price_type', table_name='tenant_subscription_history')
    op.drop_index('idx_org_sub_hist_payment_via', table_name='tenant_subscription_history')
    op.drop_index('idx_org_sub_hist_invoice_number', table_name='tenant_subscription_history')
    op.drop_index('idx_org_sub_hist_expiry_date', table_name='tenant_subscription_history')
    op.drop_table('tenant_subscription_history')
    # ### end Alembic commands ###
