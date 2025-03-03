import uuid
import random
from enum import Enum as PyEnum
from datetime import datetime, timedelta
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
    industry_type = Column(String(255), nullable=True)
    domain = Column(String(255), nullable=True)
    is_subdomain = Column(Boolean, default=True)
    currency = Column(String(3), nullable=False)
    date_format = Column(String(50), nullable=False)
    time_format = Column(String(50), nullable=False)
    time_zone = Column(String(50), nullable=False)
    otp = Column(String(6), nullable=True)
    otp_expiry_at = Column(DateTime, nullable=True)
    status = Column(Enum(TenantStatusEnum), default=TenantStatusEnum.NOT_VERIFIED)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def generate_otp(self):
        """
        Generate a 6-digit OTP and set the expiry time.
        The OTP expires in 10 minutes.
        """
        self.otp = str(random.randint(100000, 999999))  # Generate random 6-digit OTP
        self.otp_expiry_at = datetime.utcnow() + timedelta(minutes=10)  # Expiry set to 10 minutes from now

    def is_otp_expired(self):
        """
        Check if the OTP has expired.
        Returns True if expired, False otherwise.
        """
        if not self.otp_expiry_at:
            return False  # OTP is not set, so it can't be expired
        return datetime.utcnow() > self.otp_expiry_at

    # Indexes
    __table_args__ = (
        Index('idx_tenant_company_name', 'company_name'),
        Index('idx_tenant_domain', 'domain'),
        Index('idx_tenant_status', 'status'),
    )
