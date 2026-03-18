from fastapi import APIRouter, HTTPException
import os
import requests

router = APIRouter()

API_KEY = os.getenv("AERODATABOX_KEY")
API_HOST = "aerodatabox.p.rapidapi.com"

@router.get("/live/flights/{flight_number}")
def get_live_flight(flight_number: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Missing AERODATABOX_KEY")

    url = f"https://{API_HOST}/flights/number/{flight_number}"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    response = requests.get(url, headers=headers, timeout=20)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"AeroDataBox request failed: {response.text}"
        )

    return response.json()
