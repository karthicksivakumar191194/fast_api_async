from sqlalchemy import Table, Column, UUID, ForeignKey, String
from app.db.database import Base

user_team_association = Table(
    'user_team_association',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('team_id', UUID(as_uuid=True), ForeignKey('teams.id', ondelete='CASCADE'), primary_key=True),
    Column('role', String, nullable=False) # admin, user
)
