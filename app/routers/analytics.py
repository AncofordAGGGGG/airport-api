from fastapi import APIRouter, HTTPException
from ..db import SessionLocal
from ..models import Flight

router = APIRouter()

@router.get("/analytics/delay-rate")
def get_delay_rate(origin: str = None):
    db = SessionLocal()

    query = db.query(Flight)

    if origin:
        query = query.filter(Flight.origin == origin.upper())

    flights = query.all()

    if not flights:
        raise HTTPException(status_code=404, detail="No flights found")

    total_flights = len(flights)
    delayed_flights = len([f for f in flights if f.status == "delayed"])
    delay_rate = delayed_flights / total_flights

    return {
        "origin": origin.upper() if origin else "ALL",
        "total_flights": total_flights,
        "delayed_flights": delayed_flights,
        "delay_rate": delay_rate
    }

@router.get("/analytics/delay-by-hour")
def get_delay_by_hour(origin: str = None):
    db = SessionLocal()

    query = db.query(Flight)

    if origin:
        query = query.filter(Flight.origin == origin.upper())

    flights = query.all()

    if not flights:
        raise HTTPException(status_code=404, detail="No flights found")

    hourly_stats = {}

    for flight in flights:
        if not flight.scheduled_departure:
            continue

        hour = flight.scheduled_departure.hour

        if hour not in hourly_stats:
            hourly_stats[hour] = {
                "total_flights": 0,
                "delayed_flights": 0
            }

        hourly_stats[hour]["total_flights"] += 1

        if flight.status == "delayed":
            hourly_stats[hour]["delayed_flights"] += 1

    result = []

    for hour in sorted(hourly_stats.keys()):
        total = hourly_stats[hour]["total_flights"]
        delayed = hourly_stats[hour]["delayed_flights"]
        delay_rate = delayed / total if total > 0 else 0

        result.append({
            "hour": hour,
            "total_flights": total,
            "delayed_flights": delayed,
            "delay_rate": delay_rate
        })

    return {
        "origin": origin.upper() if origin else "ALL",
        "by_hour": result
    }
