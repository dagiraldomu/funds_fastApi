from fastapi import FastAPI
from app.routers import clients, funds, transactions, notifications # Import the router object


app = FastAPI(title="Fondos", description="Sistema de inversión en fondos")

# Include the router object in the application
app.include_router(clients.router, prefix="/api")
app.include_router(funds.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # Adjust host, port, and reload as needed
