from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.models.funds import FundModel, get_db
from app.schemas.funds import FundCreateSchema

router = APIRouter()

@router.get("/funds", response_model=List[FundModel])
async def fetch_funds(limit: int = 10, db = Depends(get_db)):
    return await db.funds.find().to_list(length=limit)


@router.post("/funds", response_model=FundModel)
async def create_fund(fund: FundCreateSchema,  db = Depends(get_db)):
    new_fund = fund.model_dump()
    result = await db.funds.insert_one(new_fund)
    if result.inserted_id:
        return await db.funds.find_one({"_id": result.inserted_id})
    raise HTTPException(status_code=400, detail="Error al crear el fondo")

