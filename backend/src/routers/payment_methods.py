from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from models.payment_method import PaymentMethod, PaymentMethodCreate, PaymentMethodUpdate
from dependencies import get_session

router = APIRouter()

@router.get("/", response_model=List[PaymentMethod])
async def read_payment_methods(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    payment_methods = session.exec(select(PaymentMethod).offset(skip).limit(limit)).all()
    return payment_methods

@router.get("/{payment_method_id}", response_model=PaymentMethod)
async def read_payment_method(payment_method_id: int, session: Session = Depends(get_session)):
    payment_method = session.get(PaymentMethod, payment_method_id)
    if not payment_method:
        raise HTTPException(status_code=404, detail="PaymentMethod not found")
    return payment_method

@router.post("/", response_model=PaymentMethod)
async def create_payment_method(payment_method: PaymentMethodCreate, session: Session = Depends(get_session)):
    db_payment_method = PaymentMethod.model_validate(payment_method)
    session.add(db_payment_method)
    session.commit()
    session.refresh(db_payment_method)
    return db_payment_method

@router.patch("/{payment_method_id}", response_model=PaymentMethod)
async def update_payment_method(
    payment_method_id: int,
    payment_method_update: PaymentMethodUpdate,
    session: Session = Depends(get_session)
):
    db_payment_method = session.get(PaymentMethod, payment_method_id)
    if not db_payment_method:
        raise HTTPException(status_code=404, detail="PaymentMethod not found")
    
    payment_method_data = payment_method_update.model_dump(exclude_unset=True)
    for key, value in payment_method_data.items():
        setattr(db_payment_method, key, value)
        
    session.add(db_payment_method)
    session.commit()
    session.refresh(db_payment_method)
    return db_payment_method

@router.delete("/{payment_method_id}")
async def delete_payment_method(payment_method_id: int, session: Session = Depends(get_session)):
    payment_method = session.get(PaymentMethod, payment_method_id)
    if not payment_method:
        raise HTTPException(status_code=404, detail="PaymentMethod not found")
    
    session.delete(payment_method)
    session.commit()
    return {"ok": True}
