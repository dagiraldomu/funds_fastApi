from typing import List

from fastapi import APIRouter
from app.database.database import db
from app.models.funds import NotificationModel

router = APIRouter()

@router.get("/notifications", response_model=List[NotificationModel])
async def fetch_notifications(limit: int = 10):
    return await db.notifications.find().to_list(length=limit)
