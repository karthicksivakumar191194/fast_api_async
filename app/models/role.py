import uuid
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, UUID, String, DateTime, ForeignKey, func, Index, Boolean, Enum

from app.db.database import Base


class RoleStatusEnum(PyEnum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    is_default = Column(Boolean, default=False)
    status = Column(Enum(RoleStatusEnum), default=RoleStatusEnum.ACTIVE)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    users = relationship("User", back_populates="role")

    # Indexes
    __table_args__ = (
        Index('idx_role_tenant_id', 'tenant_id'),
        Index('idx_role_name', 'name'),
    )
