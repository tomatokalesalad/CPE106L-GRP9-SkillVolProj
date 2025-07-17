from pydantic import BaseModel
from enum import Enum

# ────────────── Step 1: Enum for availability ──────────────
class Availability(str, Enum):
    morning = "Morning"
    afternoon = "Afternoon"
    evening = "Evening"
    weekend = "Weekend"

# ────────────── Step 2: Models using the Enum ──────────────
class User(BaseModel):
    name: str
    skills: str
    location: str
    availability: Availability

class Request(BaseModel):
    requester_name: str
    requested_skill: str
    location: str
    availability: Availability
