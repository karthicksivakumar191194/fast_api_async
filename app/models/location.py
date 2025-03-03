import uuid
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, UUID, ForeignKey, String, Text, Boolean, DateTime, func, Index, Enum

from app.db.database import Base
from app.models.user_location_association import user_location_association


class LocationStatusEnum(PyEnum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)

class Location(Base):
    __tablename__ = 'locations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    is_default = Column(Boolean, default=False)
    status = Column(Enum(LocationStatusEnum), default=LocationStatusEnum.ACTIVE)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    tenant = relationship('Tenant', backref='locations', lazy=True)
    users = relationship("User", secondary=user_location_association, back_populates="locations")

    # Indexes
    __table_args__ = (
        Index('idx_location_tenant_id', 'tenant_id'),
        Index('idx_location_workspace_id', 'workspace_id'),
        Index('idx_location_name', 'name'),
    )
