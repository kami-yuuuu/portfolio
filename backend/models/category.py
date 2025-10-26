from sqlmodel import Field, SQLModel, String, create_engine
from typing import Optional,List, TYPE_CHECKING
from sqlmodel import Relationship, func, Column, DateTime
from datetime import datetime

#循環参照を避けて型ヒントを提供するための条件付きインポート
if TYPE_CHECKING:
    from .transaction import Transaction


class Category(SQLModel, table=True):
    """
    取引カテゴリを表すモデル
    収入や支出などの分類に使用される

    Attributes:
        id (Optional[int]): カテゴリの一意の識別子
        name (str): カテゴリの名前
        type (str): 取引の分類（収入/支出など）
        color (str): カテゴリの色を表す16進カラーコード
        transactions (List['Transaction']): このカテゴリに関連する取引のリスト
        created_at (Optional[datetime]): 作成日時
        updated_at (Optional[datetime]): 更新日時

    """

    id:Optional[int] = Field(default=None, primary_key=True)
    name:str = Field(description="カテゴリの名前", unique=True)
    type: str = Field(description="取引の分類（収入/支出など）")
    color:str = Field(default="#FFFFFF", description="カテゴリの色を表す16進カラーコード", unique=True)
    transactions: List['Transaction'] = Relationship(back_populates="category")
    created_at: Optional[datetime] = Field(default=None, description="作成日時", sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(default=None, description="更新日時", sa_column=Column(DateTime(timezone=True), onupdate=func.now()))
