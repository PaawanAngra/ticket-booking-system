from fastapi import FastAPI, Depends, HTTPException
from . import database, models
from . import schemas

app = FastAPI(title="High concurrency ticket booking system")

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
def create_booking(booking : schemas.BookingCreate, db = Depends(database.get_db)):
    try:
        event = db.query(models.Events).filter(models.Events.id == booking.event_id).first()
        if not event or event.available_tickets <= 0:
            return HTTPException(status_code=400, detail = "No tickets for this event")
        event.total_tickets -= 1
        new_booking = models.Bookings(event_id = booking.event_id, user_id = booking.user_id, seat_number = booking.seat_number)
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail= {"error" : ""})
    return new_booking