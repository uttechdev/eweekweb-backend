from datetime import date
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List

# class Org(BaseModel):
#   id: ObjectId = Field(default_factory=ObjectId, alias="_id")
#   name: str
#   org_type: str
#   is_admin: bool

#   class Config:
#     allow_population_by_field_name = True
#     json_encoders = {
#       ObjectId: str
#     }
#     schema_extra = {
#       "example": {
#         "name": "IEEE",
#         "org_type": "small",
#         "is_admin": True
#       }
#     }
class LoginRequest(BaseModel):
    email: str
    password: str
    
class UserData(BaseModel):
    _id: str
    name: str
    email: str
    authentication: int  # Removed hashed_pw from the response model for security

# This now correctly represents the response you intend to return
class UserResponse(BaseModel):
    response: UserData  # No need for additional nesting

class Event(BaseModel):
    _id: str
    org: str
    name: str
    start_time: date
    end_time: date
    event_code: str
    location: str
    rules_link: str

class Org(BaseModel):
    _id: str
    name: str
    org_type: str
    is_admin: bool

class AttendanceForm(BaseModel):
    _id: str
    event: str
    timestamp: date
    is_signin: bool
    valid: bool
    org: str
    eid: str
    name: str
    year: str
    event_code: str
    major: str
    error_flag: str