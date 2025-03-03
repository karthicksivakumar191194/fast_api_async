import uuid
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, UUID, String, Text, DateTime, ForeignKey, func, Boolean, Index, Enum

from app.db.database import Base
from app.models.user_team_association import user_team_association


class TeamStatusEnum(PyEnum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)


class Team(Base):
    __tablename__ = 'teams'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image = Column(String(512), nullable=True)
    is_default = Column(Boolean, default=False)
    status = Column(Enum(TeamStatusEnum), default=TeamStatusEnum.ACTIVE)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    tenant = relationship('Tenant', backref='teams', lazy=True)
    users = relationship("User", secondary=user_team_association, back_populates="teams")

    # Indexes
    __table_args__ = (
        Index('idx_team_tenant_id', 'tenant_id'),
        Index('idx_team_workspace_id', 'workspace_id'),
        Index('idx_team_name', 'name'),
    )
