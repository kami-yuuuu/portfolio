from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func
from typing import List, Optional , TYPE_CHECKING
from datetime import datetime

# 循環参照を避けて型ヒントを提供するための条件付きインポート
if TYPE_CHECKING:
    from .transaction import Transaction


class PaymentMethod(SQLModel, table=True):
    """
    支払い方法を表すモデル
    クレジットカード、現金、電子マネーなどの支払い手段を管理する

    Attributes:
        id (Optional[int]): 支払い方法の一意の識別子
        name (str): 支払い方法の名前
        description (Optional[str]): 支払い方法の説明
        transactions (List['Transaction']): この支払い方法に関連する取引のリスト
        created_at (Optional[datetime]): 作成日時
        updated_at (Optional[datetime]): 更新日時
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(description="支払い方法の名前")
    description: Optional[str] = Field(default=None, description="支払い方法の説明")
    transactions: List['Transaction'] = Relationship(back_populates="payment_method")
    created_at: Optional[datetime] = Field(default=None, description="作成日時", sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(default=None, description="更新日時", sa_column=Column(DateTime(timezone=True), onupdate=func.now()))


