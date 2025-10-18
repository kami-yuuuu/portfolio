from typing import Optional, Dict, List 
from decimal import Decimal
from datetime import date as dates, datetime
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DateTime, func, JSON 
from .category import Category


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: dates = Field(description="取引日")
    category: Category  = Relationship(back_populates="transactions")
    amount: Decimal = Field(description="金額")
    memo: Optional[str] = None
    payment_method_pk: str = Field(default=None, foreign_key="paymentmethod.pk", description="支払い方法")
    repeat: Optional[Dict] = Field(default=None, description="繰り返し設定", sa_column=Column(JSON))
    receipt_url: Optional[str] = Field(default=None, description="レシート画像のURL")
    created_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), server_default=func.now()), description="作成日時")
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), onupdate=func.now()), description="更新日時")
