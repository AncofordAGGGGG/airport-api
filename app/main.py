from fastapi import FastAPI

app = FastAPI(title="Airport Delay API")

@app.get("/")
def home():
    return {"message": "Airport Delay API is running"}

from .db import engine, Base
from . import models

Base.metadata.create_all(bind=engine)

from .routers import flights

app.include_router(flights.router)
