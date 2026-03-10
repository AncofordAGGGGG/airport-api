from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Flight

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST /flights
@router.post("/flights")
def create_flight(flight_number: str, origin: str, destination: str):
    db = SessionLocal()

    flight = Flight(
        flight_number=flight_number,
        origin=origin,
        destination=destination
    )

    db.add(flight)
    db.commit()
    db.refresh(flight)

    return flight


# GET /flights/{id}
@router.get("/flights/{flight_id}")
def get_flight(flight_id: int):

    db = SessionLocal()

    flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    return flight


# PUT /flights/{id}
@router.put("/flights/{flight_id}")
def update_flight(flight_id: int, flight_number: str, origin: str, destination: str):

    db = SessionLocal()

    flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    flight.flight_number = flight_number
    flight.origin = origin
    flight.destination = destination

    db.commit()

    return flight


# DELETE /flights/{id}
@router.delete("/flights/{flight_id}")
def delete_flight(flight_id: int):

    db = SessionLocal()

    flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    db.delete(flight)
    db.commit()

    return {"message": "Flight deleted"}
