from sqlalchemy import Table, Column, UUID, ForeignKey
from app.db.database import Base

user_location_association = Table(
    'user_location_association',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('location_id', UUID(as_uuid=True), ForeignKey('locations.id', ondelete='CASCADE'), primary_key=True),
)
