from fastapi import FastAPI, Depends, Path, Body, HTTPException
from sqlmodel import Session, create_engine, select
from models.session import engine
from models.transaction import Transaction
from models.category import CategoryCreate, Category



app = FastAPI()


#dependency
async def get_session():
    with Session(engine) as session:
        yield session


@app.get("/items/{item_id}")
async def read_item(item_id:int):
    return {"item_id": item_id}

@app.get("/health")
async def return_health():
    return {"status": "ok"}


@app.get("/transaction/{transaction_id}")
async def get_transactions(transaction_id: int = Path(title="The ID of the transaction to get"),session = Depends(get_session), return_model=Transaction):
    selection = select(Transaction).where(Transaction.id == transaction_id)
    transaction = session.exec(selection).first()
    if not transaction:
        return {"error": "Transaction not found"}
    return transaction

@app.post("/transaction/")
async def create_transaction(transaction: Transaction, session = Depends(get_session)):
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@app.get("/cateegory/{category_id}")
async def get_category(category_id: int = Path(title="The ID of the category to get"),session = Depends(get_session)):
    selection = select(Category).where(Category.id == category_id)
    category = session.exec(selection).first()
    if not category:
        return {"error": "Category not found"}
    return category

@app.post("/category/")
async def create_category(category: CategoryCreate, session = Depends(get_session)):
    #category = Category.model_validate(category)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


