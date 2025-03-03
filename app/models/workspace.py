from sqlalchemy import Column, UUID, ForeignKey, String, Boolean, DateTime, func, Enum, Index
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
import uuid

from app.db.database import Base
from app.models.user_workspace_association import user_workspace_association  # Correct import

class WorkSpaceStatusEnum(PyEnum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)

class Workspace(Base):
    __tablename__ = 'workspaces'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    is_default = Column(Boolean, default=False)
    status = Column(Enum(WorkSpaceStatusEnum), default=WorkSpaceStatusEnum.ACTIVE)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    tenant = relationship('Tenant', backref='workspaces', lazy=True)
    users = relationship("User", secondary=user_workspace_association, back_populates="workspaces")  # Ensure 'User' has back_populates

    # Indexes
    __table_args__ = (
        Index('idx_workspace_tenant_id', 'tenant_id'),
    )
