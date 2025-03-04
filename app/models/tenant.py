import uuid
from enum import Enum as PyEnum
from sqlalchemy import Column, UUID, String, Text, DateTime, Boolean, func, Index, Enum

from app.db.database import Base


class TenantStatusEnum(PyEnum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")
    INACTIVE = ("inactive", "Inactive")
    NOT_VERIFIED = ("not_verified", "Not Verified")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)

class Tenant(Base):
    __tablename__ = 'tenants'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(255), nullable=False)
    company_logo = Column(String(512), nullable=True)
    company_size = Column(String(255), nullable=True)
    company_location = Column(Text, nullable=True)
    company_country = Column(String(255), nullable=True)
    industry = Column(String(255), nullable=True)
    workspace_name = Column(String(255), nullable=True)
    domain = Column(String(255), nullable=True)
    is_subdomain = Column(Boolean, default=True)
    currency = Column(String(3), nullable=False)
    date_format = Column(String(50), nullable=False)
    time_format = Column(String(50), nullable=False)
    time_zone = Column(String(50), nullable=False)
    account_owner_handle = Column(Text, nullable=True)
    solutions_interested = Column(Text, nullable=True)
    status = Column(Enum(TenantStatusEnum), default=TenantStatusEnum.NOT_VERIFIED)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Indexes
    __table_args__ = (
        Index('idx_tenant_company_name', 'company_name'),
        Index('idx_tenant_domain', 'domain'),
        Index('idx_tenant_status', 'status'),
    )
