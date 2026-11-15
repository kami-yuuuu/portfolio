from fastapi import FastAPI
from routers import transactions, categories, payment_methods

app = FastAPI(title="家計簿アプリ API", version="0.1.0")

app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(payment_methods.router, prefix="/payment_methods", tags=["payment_methods"])


@app.get("/health", tags=["health"])
def return_health():
    return {"status": "ok"}
