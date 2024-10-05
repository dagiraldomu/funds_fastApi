from pydantic import BaseModel

class ClientCreateSchema(BaseModel):
    name: str
    email: str
    phone: str
    notification_preference: str

class FundCreateSchema(BaseModel):
    name: str
    minimum_investment: float
    category: str

class TransactionCreateSchema(BaseModel):
    client_id: str
    fund_id: str
    amount: float

class TransactionCancellationSchema(BaseModel):
    client_id: str
    fund_id: str


class NotificationCreateSchema(BaseModel):
    client_id: str
    fund_id: str
    type: str  # subscription | cancellation
    notification_method: str
    message: str
