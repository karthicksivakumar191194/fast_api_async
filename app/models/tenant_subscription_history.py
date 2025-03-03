from sqlalchemy import Column, UUID, Numeric, String, DateTime, Date, Integer, ForeignKey, func, Index, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum as PyEnum
import uuid

from app.db.database import Base

class SubscriptionHistoryStatusEnum(PyEnum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")
    IN_ACTIVE = ("in_active", "In Active")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)

class TenantSubscriptionHistory(Base):
    __tablename__ = 'tenant_subscription_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    subscription_plan = Column(UUID(as_uuid=True), ForeignKey('subscription_plans.id', ondelete='CASCADE'), nullable=False)
    price_month_rupee = Column(Numeric(10, 2), nullable=False)
    price_year_rupee = Column(Numeric(10, 2), nullable=False)
    price_month_dollar = Column(Numeric(10, 2), nullable=False)
    price_year_dollar = Column(Numeric(10, 2), nullable=False)
    details = Column(JSONB, default={})
    plan_type = Column(String(255), nullable=False)
    plan_price_type = Column(String(255), nullable=False)
    invoice_number = Column(Integer, unique=True, nullable=False)
    invoice_url = Column(String(255), nullable=True)
    start_timestamp = Column(DateTime, nullable=True)
    end_timestamp = Column(DateTime, nullable=True)
    payment_via = Column(String(255), nullable=False)
    expiry_days = Column(Integer, nullable=True)
    expiry_date = Column(Date, nullable=True)
    status = Column(Enum(SubscriptionHistoryStatusEnum), default=SubscriptionHistoryStatusEnum.IN_ACTIVE)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    tenant = relationship('Tenant', backref='tenant_subscription_history', lazy=True)
    subscription_plan_rel = relationship('SubscriptionPlan', backref='plan_subscription_history', lazy=True)

    # Indexes
    __table_args__ = (
        Index('idx_org_sub_hist_tenant_id', 'tenant_id'),
        Index('idx_org_sub_hist_subscription_plan', 'subscription_plan'),
        Index('idx_org_sub_hist_invoice_number', 'invoice_number'),
        Index('idx_org_sub_hist_plan_type', 'plan_type'),
        Index('idx_org_sub_hist_plan_price_type', 'plan_price_type'),
        Index('idx_org_sub_hist_payment_via', 'payment_via'),
        Index('idx_org_sub_hist_status', 'status'),
        Index('idx_org_sub_hist_expiry_date', 'expiry_date'),
    )
