from fastapi import FastAPI
from routers import transactions, categories, payment_methods

app = FastAPI()

app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(payment_methods.router, prefix="/payment_methods", tags=["payment_methods"])

@app.get("/health")
async def return_health():
    return {"status": "ok"}
