from pydantic import BaseModel
from enum import Enum

# ────────────── Step 1: Enum for availability ──────────────
class Availability(str, Enum):
    weekdays = "Weekdays"
    weekends = "Weekends"
    evening = "Evening"
    fulltime = "Full-time"
    flexible = "Flexible"

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
