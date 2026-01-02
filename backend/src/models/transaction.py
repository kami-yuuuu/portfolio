from typing import Optional, Dict
from datetime import date as dates, datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from sqlalchemy import DateTime, func, Numeric
from .category import Category
from .payment_method import PaymentMethod

class Transaction(SQLModel, table=True):
    """
    取引を表すモデル
    個々の収入や支出の記録を管理する

    Attributes:
        id (Optional[int]): 取引の一意の識別子
        date (date): 取引日
        category_id (int): カテゴリID
        category (Category): 関連するカテゴリオブジェクト
        amount (Decimal): 取引金額(¥)
        memo (Optional[str]): 取引のメモ
        payment_method_id (int): 支払い方法
        payment_method (Optional[PaymentMethod]): 関連する支払い方法オブジェクト
        repeat (Dict): 繰り返し設定
        receipt_url (Optional[str]): レシート画像のURL
        created_at (Optional[datetime]): 作成日時
        updated_at (Optional[datetime]): 更新日時
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    date: dates = Field(description="取引日")
    category_id: int = Field(foreign_key="category.id", description="カテゴリID")
    category: Optional[Category] = Relationship(back_populates="transactions")
    amount: Decimal = Field(description="取引金額(¥)", sa_column=Column(Numeric(12, 2)))
    memo: Optional[str] = None
    payment_method_id: int = Field(default=None, foreign_key="paymentmethod.id", description="支払い方法")
    payment_method: Optional["PaymentMethod"] = Relationship(back_populates="transactions")
    repeat: Dict = Field(description="繰り返し設定", default_factory=dict, sa_column=Column(JSON))
    receipt_url: Optional[str] = Field(default=None, description="レシート画像のURL")
    created_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), server_default=func.now()), description="作成日時")
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), onupdate=func.now()), description="更新日時")


class TransactionCreate(SQLModel):
    """
    取引作成用モデル
    新しい取引を作成するためのデータ構造を定義する
    """
    date: dates = Field(description="取引日")
    category_id: int = Field(description="カテゴリID")
    amount: Decimal = Field(description="取引金額")
    memo: Optional[str] = None
    payment_method_id: int = Field(description="支払い方法")
    repeat: Dict = Field(description="繰り返し設定", default_factory=dict)
    receipt_url: Optional[str] = Field(default=None, description="レシート画像のURL")


class TransactionUpdate(SQLModel):
    """
    取引更新用モデル
    """
    date: Optional[dates] = None
    category_id: Optional[int] = None
    amount: Optional[Decimal] = None
    memo: Optional[str] = None
    payment_method_id: Optional[int] = None
    repeat: Optional[Dict] = None
    receipt_url: Optional[str] = None
