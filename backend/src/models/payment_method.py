from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func

if TYPE_CHECKING:
    from .transaction import Transaction


class BasePaymentMethod(SQLModel):
    name: str = Field(min_length=1, max_length=100, description="支払い方法の名前")
    description: Optional[str] = Field(default=None, max_length=500, description="支払い方法の説明")


class PaymentMethod(BasePaymentMethod, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, min_length=1, max_length=100)
    transactions: List['Transaction'] = Relationship(back_populates="payment_method")
    created_at: Optional[datetime] = Field(default=None, description="作成日時", sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(default=None, description="更新日時", sa_column=Column(DateTime(timezone=True), onupdate=func.now()))


class PaymentMethodCreate(BasePaymentMethod):
    pass


class PaymentMethodUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)


class PaymentMethodRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
