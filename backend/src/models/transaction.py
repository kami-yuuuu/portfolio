from typing import Optional, Dict, Any
from datetime import date as dates, datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from sqlalchemy import DateTime, func, Numeric
from .category import Category
from .payment_method import PaymentMethod


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: dates = Field(description="取引日")
    category_id: int = Field(foreign_key="category.id", description="カテゴリID")
    category: Optional[Category] = Relationship(back_populates="transactions")
    amount: Decimal = Field(description="取引金額(¥)", sa_column=Column(Numeric(12, 2)))
    memo: Optional[str] = Field(default=None, max_length=1000)
    payment_method_id: Optional[int] = Field(default=None, foreign_key="paymentmethod.id", description="支払い方法")
    payment_method: Optional[PaymentMethod] = Relationship(back_populates="transactions")
    repeat: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    receipt_url: Optional[str] = Field(default=None, max_length=2048, description="レシート画像のURL")
    created_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), onupdate=func.now()))


class TransactionCreate(SQLModel):
    date: dates = Field(description="取引日")
    category_id: int = Field(gt=0, description="カテゴリID")
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2, description="取引金額")
    memo: Optional[str] = Field(default=None, max_length=1000)
    payment_method_id: int = Field(gt=0, description="支払い方法")
    repeat: Dict[str, Any] = Field(default_factory=dict)
    receipt_url: Optional[str] = Field(default=None, max_length=2048)


class TransactionUpdate(SQLModel):
    date: Optional[dates] = None
    category_id: Optional[int] = Field(default=None, gt=0)
    amount: Optional[Decimal] = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    memo: Optional[str] = Field(default=None, max_length=1000)
    payment_method_id: Optional[int] = Field(default=None, gt=0)
    repeat: Optional[Dict[str, Any]] = None
    receipt_url: Optional[str] = Field(default=None, max_length=2048)


class TransactionRead(SQLModel):
    id: int
    date: dates
    category_id: int
    amount: Decimal
    memo: Optional[str] = None
    payment_method_id: Optional[int] = None
    repeat: Dict[str, Any]
    receipt_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
