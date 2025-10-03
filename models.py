from pydantic import BaseModel
from typing import Optional

# Create class
class Observation(BaseModel):
    city: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    windspeed: float
    observation_time: str