from typing import Optional, Dict
from datetime import date as dates, datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from sqlalchemy import DateTime, func
from .category import Category
from .payment_method import PaymentMethod



class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: dates = Field(description="取引日")
    category_id: int = Field(foreign_key="category.id", description="カテゴリID")
    category: Category  = Relationship(back_populates="transactions")
    amount: Decimal = Field(description="取引金額")
    memo: Optional[str] = None
    payment_method_id: int = Field(default=None, foreign_key="paymentmethod.id", description="支払い方法")
    payment_method: Optional["PaymentMethod"] = Relationship(back_populates="transactions")
    repeat: Dict = Field(description="繰り返し設定", default_factory=dict, sa_column=Column(JSON))
    receipt_url: Optional[str] = Field(default=None, description="レシート画像のURL")
    created_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), server_default=func.now()), description="作成日時")
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), onupdate=func.now()), description="更新日時")
