from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List

from models.payment_method import PaymentMethod, PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodRead
from dependencies import get_session
from database_errors import commit_or_conflict

router = APIRouter()


@router.get("/", response_model=List[PaymentMethodRead])
def read_payment_methods(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(PaymentMethod).offset(skip).limit(limit)).all()


@router.get("/{payment_method_id}", response_model=PaymentMethodRead)
def read_payment_method(payment_method_id: int, session: Session = Depends(get_session)):
    if payment_method_id <= 0:
        raise HTTPException(status_code=422, detail="payment_method_id must be greater than zero")
    payment_method = session.get(PaymentMethod, payment_method_id)
    if payment_method is None:
        raise HTTPException(status_code=404, detail="PaymentMethod not found")
    return payment_method


@router.post("/", response_model=PaymentMethodRead, status_code=201)
def create_payment_method(payment_method: PaymentMethodCreate, session: Session = Depends(get_session)):
    db_payment_method = PaymentMethod.model_validate(payment_method)
    session.add(db_payment_method)
    commit_or_conflict(session)
    session.refresh(db_payment_method)
    return db_payment_method


@router.patch("/{payment_method_id}", response_model=PaymentMethodRead)
def update_payment_method(
    payment_method_id: int,
    payment_method_update: PaymentMethodUpdate,
    session: Session = Depends(get_session),
):
    if payment_method_id <= 0:
        raise HTTPException(status_code=422, detail="payment_method_id must be greater than zero")
    db_payment_method = session.get(PaymentMethod, payment_method_id)
    if db_payment_method is None:
        raise HTTPException(status_code=404, detail="PaymentMethod not found")
    for key, value in payment_method_update.model_dump(exclude_unset=True).items():
        setattr(db_payment_method, key, value)
    session.add(db_payment_method)
    commit_or_conflict(session)
    session.refresh(db_payment_method)
    return db_payment_method


@router.delete("/{payment_method_id}", response_model=dict[str, bool])
def delete_payment_method(payment_method_id: int, session: Session = Depends(get_session)):
    if payment_method_id <= 0:
        raise HTTPException(status_code=422, detail="payment_method_id must be greater than zero")
    payment_method = session.get(PaymentMethod, payment_method_id)
    if payment_method is None:
        raise HTTPException(status_code=404, detail="PaymentMethod not found")
    session.delete(payment_method)
    commit_or_conflict(session)
    return {"ok": True}
