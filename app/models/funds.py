from typing import List, Optional
from datetime import datetime
from typing import Annotated, Any, Callable

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic_core import core_schema
from app.database.database import db as mongo_db


def get_db():
    db = mongo_db
    yield db


class _ObjectIdPydanticAnnotation:
    # Based on https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types.

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(input_value: str) -> ObjectId:
            return ObjectId(input_value)

        return core_schema.union_schema(
            [
                # check if it's an instance first before doing any further work
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ],
            serialization=core_schema.to_string_ser_schema(),
        )

PydanticObjectId = Annotated[
    ObjectId, _ObjectIdPydanticAnnotation
]


# Transacción Model
class TransactionModel(BaseModel):
    id: PydanticObjectId = Field(description="MongoDB document ObjectID", alias='_id')
    client_id: PydanticObjectId
    fund_id: PydanticObjectId
    type: str  # subscription or cancellation
    amount: float
    transaction_date: datetime = datetime.now()
    balance_after_transaction: float


    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


# Cliente Model
class ClientModel(BaseModel):
    id: PydanticObjectId = Field(description="MongoDB document ObjectID", alias='_id')
    name: str
    email: str
    phone: str
    balance: float = 500000
    subscriptions: List[dict] = []
    notification_preference: str # email | phone

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# Fondo Model
class FundModel(BaseModel):
    id: PydanticObjectId = Field(description="MongoDB document ObjectID", alias='_id')
    name: str
    minimum_investment: float
    category: str

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}



# Notificación Model
class NotificationModel(BaseModel):
    id: PydanticObjectId = Field(description="MongoDB document ObjectID", alias='_id')
    client_id: PydanticObjectId
    fund_id: PydanticObjectId
    type: str  # subscription or cancellation
    notification_method: str  # email | phone
    message: str
    sent_at: datetime = datetime.now()

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
