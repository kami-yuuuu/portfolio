from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from .transaction import Transaction


class PaymentMethod(SQLModel, table=True):
    name: Optional[str]= Field(default=None, primary_key=True, description="支払い方法の名前")
    description: Optional[str] = Field(default=None, description="支払い方法の説明")
    
