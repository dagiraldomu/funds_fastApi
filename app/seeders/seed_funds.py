import asyncio
from app.schemas.funds import FundCreateSchema
from app.database.database import db

funds_collection = db.funds

# Initial funds for the seeder
initial_funds = [
    FundCreateSchema(name="FPV_BTG_PACTUAL_RECAUDADORA", minimum_investment=75000, category="FPV"),
    FundCreateSchema(name="FPV_BTG_PACTUAL_ECOPETROL", minimum_investment=125000, category="FPV"),
    FundCreateSchema(name="DEUDAPRIVADA", minimum_investment=50000, category="FIC"),
    FundCreateSchema(name="FDO-ACCIONES", minimum_investment=250000, category="FIC"),
    FundCreateSchema(name="FPV_BTG_PACTUAL_DINAMICA", minimum_investment=100000, category="FPV")
]


# Function to insert funds into the database only if they don't already exist
async def seed_funds():
    for fund in initial_funds:
        # Check if the fund already exists in the database by name
        existing_fund = await funds_collection.find_one({"name": fund.name})

        if existing_fund:
            print(f"Fondo '{fund.name}' ya existe, no se insertará.")
        else:
            # Convert Pydantic data to dictionary and insert into the database
            fund_data = fund.model_dump()
            result = await funds_collection.insert_one(fund_data)
            print(f"Fondo '{fund.name}' insertado con ID: {result.inserted_id}")


# Execute seeder
if __name__ == "__main__":
    asyncio.run(seed_funds())
