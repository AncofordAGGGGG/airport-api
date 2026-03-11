from sqlalchemy import Column, Integer, String, DateTime
from .db import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String)
    origin = Column(String)
    destination = Column(String)
    scheduled_departure = Column(DateTime)
    actual_departure = Column(DateTime)
    status = Column(String, default="on_time")
