from typing import List
from fastapi import APIRouter, Depends
from app.models.funds import NotificationModel, get_db

router = APIRouter()

@router.get("/notifications", response_model=List[NotificationModel])
async def fetch_notifications(limit: int = 10, db = Depends(get_db)):
    return await db.notifications.find().to_list(length=limit)
