from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from . import database, models, schemas, redis_client

@asynccontextmanager
async def lifespan(app : FastAPI):
    r = redis_client.get_redis()
    gen = database.get_db()
    db = next(gen)
    events = db.query(models.Events).all()
    db.close()
    for event in events:
        id = event.id
        flag = r.set(f"events:{id}", event.available_tickets, nx = True)
        if flag:
            print(f"Successfully set {event.name} to {event.available_tickets}")
        else:
            available_tickets = r.get(f"events:{id}")
            print(f"Event with {id} already present with tickets - {available_tickets}")
    yield

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
    if r.get(key) is None:
        event = db.query(models.Events).filter(models.Events.id == booking.event_id).first()
        if not event:
            return HTTPException(status_code=404, detail = "No tickets for this event")
        r.set(key, event.available_tickets)
        print(f"Successfully set {event.name} to {event.available_tickets}")
    remaining = r.decr(key)
    if remaining < 0:
        r.incr(key)
        return HTTPException(status_code=400, detail = "Sold out!")
    try:
        new_booking = models.Bookings(user_id = booking.user_id, event_id = booking.event_id, seat_number = remaining + 1)
        db.add(new_booking)
        event = db.query(models.Events).filter(models.Events.id == booking.event_id).first()
        event.available_tickets -= 1
        db.commit()
        db.refresh(new_booking)
        return new_booking
    except Exception as e:
        r.incr(key)
        db.rollback()
        raise HTTPException(status_code=500, detail= str(e))