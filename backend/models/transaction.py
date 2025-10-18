from typing import Optional, TYPE_CHECKING
from datetime import date as dates, datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Numeric, DateTime, func, JSON as SA_JSON

if TYPE_CHECKING:
    from .category import Category


class Transaction(SQLModel, table=True):
    """取引情報を管理するモデル"""
    id: Optional[int] = Field(default=None, primary_key=True)
    date: dates = Field(description="取引日")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", description="カテゴリID")
    category: Optional["Category"] = Relationship(back_populates="transactions")
    amount: Decimal = Field(description="金額", sa_column=Column(Numeric(12, 2)))
    memo: Optional[str] = Field(default=None, description="メモ")
    payment_method_id: Optional[int] = Field(default=None, foreign_key="paymentmethod.id", description="支払い方法ID")
    repeat: Optional[dict] = Field(default=None, description="繰り返し設定", sa_column=Column(SA_JSON))
    receipt_url: Optional[str] = Field(default=None, description="レシート画像のURL")
    created_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), server_default=func.now()), description="作成日時")
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), onupdate=func.now()), description="更新日時")
