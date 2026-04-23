from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from . import database, models, schemas, redis_client
from sqlalchemy import func

@asynccontextmanager
async def lifespan(app : FastAPI):
    r = redis_client.get_redis()
    gen = database.get_db()
    db = next(gen)
    events = db.query(models.Events).all()
    for event in events:
        id = event.id
        available_tickets = event.total_tickets - db.query(func.count(models.Bookings.id)).filter(models.Bookings.event_id == id).scalar()
        event.available_tickets = available_tickets
        flag = r.set(f"events:{id}", available_tickets)
        if flag:
            print(f"Successfully set {event.name} to {event.available_tickets}")
    yield
    events = db.query(models.Events).all()
    for event in events:
        id = event.id
        available_tickets = event.total_tickets - db.query(func.count(models.Bookings.id)).filter(models.Bookings.event_id == id).scalar()
        event.available_tickets = available_tickets
    db.close()

app = FastAPI(title="High concurrency ticket booking system", lifespan=lifespan)

models.Base.metadata.create_all(bind = database.engine)


@app.get('/')
def health_check():
    return {'status' : 'ok'}

@app.get('/events')
def list_events(db  = Depends(database.get_db)):
    return(db.query(models.Events).all())

@app.get('/events/{event_id}')
def get_specific_event(event_id : int, db = Depends(database.get_db)):
    event = db.query(models.Events).filter(models.Events.id == event_id).first()
    if not event:
        return HTTPException(status_code=404, detail="Event not found")
    else:
        return event

@app.post('/book', response_model = schemas.Booking)
def create_booking(booking : schemas.BookingCreate, db = Depends(database.get_db), r = Depends(redis_client.get_redis)):
    key = f"events:{booking.event_id}"
    remaining = r.decr(key)
    if remaining < 0:
        r.incr(key)
        raise HTTPException(status_code=400, detail = "Sold out! or Event doesn't exist")
    try:
        new_booking = models.Bookings(user_id = booking.user_id, event_id = booking.event_id, seat_number = remaining + 1)
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking
    except Exception as e:
        r.incr(key)
        db.rollback()
        raise HTTPException(status_code=500, detail= str(e))