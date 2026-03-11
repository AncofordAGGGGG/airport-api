from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..db import SessionLocal
from ..models import Flight

router = APIRouter()

@router.post("/flights")
def create_flight(
    flight_number: str,
    origin: str,
    destination: str,
    scheduled_departure: datetime,
    actual_departure: datetime | None = None,
    status: str = "on_time"
):
    db = SessionLocal()

    flight = Flight(
        flight_number=flight_number,
        origin=origin,
        destination=destination,
        scheduled_departure=scheduled_departure,
        actual_departure=actual_departure,
        status=status
    )

    db.add(flight)
    db.commit()
    db.refresh(flight)

    return flight


@router.get("/flights/{flight_id}")
def get_flight(flight_id: int):
    db = SessionLocal()

    flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    return flight


@router.put("/flights/{flight_id}")
def update_flight(
    flight_id: int,
    flight_number: str,
    origin: str,
    destination: str,
    scheduled_departure: datetime,
    actual_departure: datetime | None = None,
    status: str = "on_time"
):
    db = SessionLocal()

    flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    flight.flight_number = flight_number
    flight.origin = origin
    flight.destination = destination
    flight.scheduled_departure = scheduled_departure
    flight.actual_departure = actual_departure
    flight.status = status

    db.commit()
    db.refresh(flight)

    return flight


@router.delete("/flights/{flight_id}")
def delete_flight(flight_id: int):
    db = SessionLocal()

    flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    db.delete(flight)
    db.commit()

    return {"message": "Flight deleted"}
