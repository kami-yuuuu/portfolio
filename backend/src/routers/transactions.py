from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List

from models.transaction import Transaction, TransactionCreate, TransactionUpdate, TransactionRead
from dependencies import get_session
from database_errors import commit_or_conflict

router = APIRouter()


@router.get("/", response_model=List[TransactionRead])
def read_transactions(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Transaction).offset(skip).limit(limit)).all()


@router.get("/{transaction_id}", response_model=TransactionRead)
def read_transaction(transaction_id: int = Query(gt=0), session: Session = Depends(get_session)):
    transaction = session.get(Transaction, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.post("/", response_model=TransactionRead, status_code=201)
def create_transaction(transaction: TransactionCreate, session: Session = Depends(get_session)):
    db_transaction = Transaction.model_validate(transaction)
    session.add(db_transaction)
    commit_or_conflict(session)
    session.refresh(db_transaction)
    return db_transaction


@router.patch("/{transaction_id}", response_model=TransactionRead)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    session: Session = Depends(get_session),
):
    if transaction_id <= 0:
        raise HTTPException(status_code=422, detail="transaction_id must be greater than zero")
    db_transaction = session.get(Transaction, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in transaction_update.model_dump(exclude_unset=True).items():
        setattr(db_transaction, key, value)
    session.add(db_transaction)
    commit_or_conflict(session)
    session.refresh(db_transaction)
    return db_transaction


@router.delete("/{transaction_id}", response_model=dict[str, bool])
def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    if transaction_id <= 0:
        raise HTTPException(status_code=422, detail="transaction_id must be greater than zero")
    transaction = session.get(Transaction, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    session.delete(transaction)
    commit_or_conflict(session)
    return {"ok": True}
