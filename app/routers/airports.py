from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Flight

router = APIRouter()

@router.get("/airports/{iata}/destinations")
def get_destinations(iata: str):

    db = SessionLocal()

    flights = db.query(Flight).filter(Flight.origin == iata.upper()).all()

    if not flights:
        raise HTTPException(status_code=404, detail="No destinations found")

    destinations = list(set([flight.destination for flight in flights]))

    return {
        "airport": iata.upper(),
        "destinations": destinations
    }
