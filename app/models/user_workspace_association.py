from sqlalchemy import Table, Column, UUID, ForeignKey
from app.db.database import Base

user_workspace_association = Table(
    'user_workspace_association',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('workspace_id', UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), primary_key=True)
)
