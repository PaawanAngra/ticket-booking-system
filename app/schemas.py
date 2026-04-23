from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    name: str
    total_tickets: int
    available_tickets: int

class Event(EventBase):
    id: int
    version: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    event_id: int
    user_id: int

class Booking(BookingCreate):
    id: int
    seat_number: int
    booked_at: datetime

    class Config:
        from_attributes = True