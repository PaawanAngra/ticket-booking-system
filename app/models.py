from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Events(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    total_tickets = Column(Integer, nullable=False)
    available_tickets = Column(Integer, nullable=False)
    version = Column(Integer, default=1)

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

class Bookings(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index = True)
    event_id = Column(Integer, ForeignKey(Events.id), nullable=False)
    user_id = Column(Integer, ForeignKey(Users.id), nullable=False)
    seat_number = Column(Integer, nullable=False)
    booked_at = Column(TIMESTAMP, server_default=func.now())
