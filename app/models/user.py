from sqlalchemy import Column, UUID, ForeignKey, String, Boolean, DateTime, func, Enum, Index
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
import uuid

from app.db.database import Base
from app.models.user_team_association import user_team_association
from app.models.user_workspace_association import user_workspace_association
from app.models.user_location_association import user_location_association


class UserStatusEnum(PyEnum):
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

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(30), nullable=True)
    password = Column(String(255), nullable=False)
    image = Column(String(512), nullable=True)
    designation = Column(String(255), nullable=True)
    primary_language = Column(String(50), default="en", nullable=True)
    is_account_owner = Column(Boolean, default=False)
    status = Column(Enum(UserStatusEnum), default=UserStatusEnum.NOT_VERIFIED)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    role = relationship("Role", back_populates="users")
    teams = relationship("Team", secondary=user_team_association, back_populates="users")
    workspaces = relationship("Workspace", secondary=user_workspace_association, back_populates="users")
    locations = relationship("Location", secondary=user_location_association, back_populates="users")

    # Indexes
    __table_args__ = (
        Index('idx_user_tenant_id', 'tenant_id'),
        Index('idx_user_email', 'email'),
        Index('idx_user_phone_number', 'phone_number'),
    )
