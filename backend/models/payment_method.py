from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from .transaction import Transaction


class PaymentMethod(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(description="支払い方法の名前")
    description: Optional[str] = Field(default=None, description="支払い方法の説明")
    created_at: Optional[str] = Field(default=None, description="作成日時")
    updated_at: Optional[str] = Field(default=None, description="更新日時")


