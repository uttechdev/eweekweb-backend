from fastapi import APIRouter, HTTPException, status, Body
import re
# from app.models import Org
from app.mongo_connection import mongo_client, orgs_global
from bson import ObjectId
from typing import List, Dict, Any
from passlib.context import CryptContext
from app.models import UserData, UserResponse, LoginRequest, AttendanceForm
from app.utils import serialize_document, extract_url_from_html

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





@router.get("/orgs", response_model=Dict[str, List[Any]])  # Fix: Enclose type annotation in quotes
async def get_orgs():
  async with mongo_client() as client:
    db = client.get_database("eweek-staging")  # Replace 'your_database_name' with the actual name of your MongoDB database
    orgs = db.org.find()
    serialized_orgs = []
    async for org in orgs:
      # serialized_org = {**org, "_id": str(org["_id"])}
      serialized_org = serialize_document(org)
      serialized_orgs.append(serialized_org)
    return {"response": serialized_orgs}
  
@router.get("/events", response_model=Dict[str, List[Any]])
async def get_events():
  async with mongo_client() as client:
    db = client.get_database("eweek-staging")
    
    pipeline = [
      {
        "$sort": {"start_time": 1}  # Add this line to sort by start_time in ascending order.
      },
      {
        "$lookup": {
          "from": "org",  # The collection to join.
          "localField": "org",  # The field from the events collection.
          "foreignField": "_id",  # The field from the org collection.
          "as": "org_info"  # The array to which the matched documents will be added.
        }
      },
      {
        "$unwind": "$org_info"  # Deconstructs the org_info array.
      },
      {
        "$project": {
          "org": "$org_info.name",  # Replace the org field with the organization's name.
          "name": 1,
          "start_time": 1,
          "end_time": 1,
          "event_code": 1,
          "location": 1,
          "rules_link": 1,
        }
      }
    ]
    
    events_cursor = db.event.aggregate(pipeline)
    serialized_events = []

    async for event in events_cursor:
      serialized_event = serialize_document(event)
      rules_link = serialized_event.get("rules_link", "")
      if rules_link:
        serialized_event["rules_link"] = extract_url_from_html(rules_link)
      serialized_events.append(serialized_event)
    
    return {"response": serialized_events}


  
@router.post("/login", response_model=UserResponse)  # Adjust the response model annotation
async def login(login_request: LoginRequest):
    async with mongo_client() as client:
        db = client["eweek-staging"]
        users_collection = db.auth_user
        user_document = await users_collection.find_one({"email": login_request.email})
        if not user_document:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Assuming pwd_context.verify() correctly verifies the password
        if not pwd_context.verify(login_request.password, user_document.get("hashed_pw", "")):
            raise HTTPException(status_code=400, detail="Incorrect password")
        
        user_data = serialize_document(user_document)
        # Make sure to not include sensitive data like the password in the response
        del user_data["hashed_pw"]
        return {"response": user_data}  # This matches the UserResponse model

@router.post("/attendance_form", response_model=Dict[str, List[Any]])
async def post_attendance(form: AttendanceForm):
  async with mongo_client() as client:
    pass