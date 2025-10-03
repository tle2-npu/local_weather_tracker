from pydantic import BaseModel
from typing import Optional

# Create subclass
class Observation(BaseModel):
    city: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    windspeed: float
    observation_time: str 