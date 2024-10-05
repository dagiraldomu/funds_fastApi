from fastapi import APIRouter, HTTPException
from app.database.database import db
from app.models.funds import TransactionModel
from app.schemas.funds import TransactionCreateSchema, TransactionCancellationSchema
from datetime import datetime
from bson import ObjectId
from typing import List
from app.services.mail_service import send_email
from app.services.sms_service import send_sms
from app.settings.config import settings

router = APIRouter()

@router.get("/transactions/{client_id}", response_model=List[TransactionModel])
async def fetch_transactions_by_user(client_id: str, limit: int = 10):
    client = await db.clients.find_one({"_id": ObjectId(client_id)})
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Retornar la transacción creada
    return await db.transactions.find({"client_id": client_id}).sort("transaction_date", -1).to_list(length=limit)

@router.post("/transactions/subscription", response_model=TransactionModel)
async def create_transaction(transaction: TransactionCreateSchema):
    # Obtener cliente y fondo de la base de datos
    client = await db.clients.find_one({"_id": ObjectId(transaction.client_id) })
    fund = await db.funds.find_one({"_id": ObjectId(transaction.fund_id)})
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if fund is None:
        raise HTTPException(status_code=404, detail="Fondo no encontrado")

    if 'subscriptions' in client:
        for subscription in client['subscriptions']:
            if subscription['fund_id'] == transaction.fund_id:
                raise HTTPException(status_code=400, detail="Ya te encuentras suscrito a este fondo")

    # Validar si el cliente tiene saldo suficiente
    if client["balance"] < fund["minimum_investment"] or client["balance"] < transaction.amount or transaction.amount < fund["minimum_investment"]:
        raise HTTPException(
            status_code=400,
            detail=f"No tiene saldo disponible para vincularse al fondo {fund['name']} o no cumple la cantidad mínima. Saldo actual: {client['balance']}, Monto mínimo requerido: {fund['minimum_investment']}, Monto solicitado: {transaction.amount}"
        )

    new_balance = client["balance"] - transaction.amount

    # Crear transacción si cumple con el saldo
    new_transaction = {
        "client_id": transaction.client_id,
        "fund_id": transaction.fund_id,
        "type": "subscription",
        "amount": transaction.amount,
        "transaction_date": datetime.now(),
        "balance_after_transaction": new_balance
    }

    # Insertar la transacción
    result = await db.transactions.insert_one(new_transaction)

    new_subscription = {
        "fund_id": transaction.fund_id,
        "date":  new_transaction['transaction_date'],
        "amount":  transaction.amount
    }

    # Actualizar el saldo del cliente
    await db.clients.update_one(
        {"_id": ObjectId(transaction.client_id)},
        {
            "$set": {"balance": new_balance},
            "$push": {"subscriptions": new_subscription}
        },
        upsert=True
    )

    new_notification = {
        "client_id": transaction.client_id,
        "fund_id": transaction.fund_id,
        "type": "subscription",
        "message": f"Acaba se suscribirse al fondo: {fund['name']}, con un monto de: COP ${transaction.amount}"
    }

    if 'email' in client["notification_preference"]:
        new_notification['notification_method'] = 'email'

        subject = "Notificación nueva suscripción a fondo"
        body_text = "Mensaje de nueva suscripción"
        body_html = f"""
        <html>
        <head></head>
        <body>
          <h1>Nueva suscripción a fondo</h1>
          <p>{new_notification['message']}.</p>
        </body>
        </html>
        """

        send_email(settings.aws_email, client['email'], subject, body_text, body_html)

    else:
        new_notification['notification_method'] = 'phone'

        send_sms(client['phone'], new_notification['message'])

    await db.notifications.insert_one(new_notification)


    # Retornar la transacción creada
    return await db.transactions.find_one({"_id": result.inserted_id})


@router.post("/transactions/cancellation", response_model=TransactionModel)
async def cancel_transaction(transaction: TransactionCancellationSchema):
    # Obtener cliente y fondo de la base de datos
    client = await db.clients.find_one({"_id": ObjectId(transaction.client_id) })
    fund = await db.funds.find_one({"_id": ObjectId(transaction.fund_id)})

    if client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if fund is None:
        raise HTTPException(status_code=404, detail="Fondo no encontrado")

    # Validar si el cliente está suscrito al fondo
    if 'subscriptions' in client:
        for subscription in client['subscriptions']:
            if subscription['fund_id'] == transaction.fund_id:

                new_balance = client["balance"] + subscription['amount']
                new_transaction = {
                    "client_id": transaction.client_id,
                    "fund_id": transaction.fund_id,
                    "type": "cancellation",
                    "amount": subscription['amount'],
                    "transaction_date": datetime.now(),
                    "balance_after_transaction": new_balance
                }

                # Insertar la transacción
                result = await db.transactions.insert_one(new_transaction)

                # Actualizar el saldo del cliente
                await db.clients.update_one(
                    {"_id": ObjectId(transaction.client_id)},
                    {
                        "$set": {"balance": new_balance},
                        "$pull": {"subscriptions": {"fund_id": subscription['fund_id']}}
                    }
                )

                # Retornar la transacción creada
                return await db.transactions.find_one({"_id": result.inserted_id})

        raise HTTPException(status_code=404, detail="El fondo solicitado no se encuentra asociado al cliente")
    else:
        raise HTTPException(status_code=404, detail="No tiene fondos asociados")
