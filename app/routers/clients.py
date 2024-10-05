from typing import List
from fastapi import APIRouter, HTTPException
from app.database.database import db
from app.models.funds import ClientModel
from app.schemas.funds import ClientCreateSchema

router = APIRouter()


@router.get("/clients", response_model=List[ClientModel])
async def fetch_users(limit: int = 10):
    return await db.clients.find().to_list(length=limit)

@router.post("/clients", response_model=ClientModel)
async def create_client(client: ClientCreateSchema):
    new_client = client.model_dump()
    new_client['balance'] = 500000  # Monto inicial
    result = await db.clients.insert_one(new_client)
    if result.inserted_id:
        return await db.clients.find_one({"_id": result.inserted_id})
    raise HTTPException(status_code=400, detail="Error al crear el cliente")
