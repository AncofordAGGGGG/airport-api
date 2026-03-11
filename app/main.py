from fastapi import FastAPI
from .db import Base, engine
from .routers import flights, airports, analytics

app = FastAPI(title="Airport Delay API")

Base.metadata.create_all(bind=engine)

app.include_router(flights.router)
app.include_router(airports.router)
app.include_router(analytics.router)

@app.get("/")
def home():
    return {"message": "Airport Delay API running"}
