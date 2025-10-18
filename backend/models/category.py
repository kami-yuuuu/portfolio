from sqlmodel import Field, SQLModel, String, create_engine
from typing import Optional
from sqlmodel import Relationship
from .transaction import Transaction


class Category(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    name:str = Field(description="カテゴリの名前", unique=True)
    type: str = Field(description="取引の分類（収入/支出など）")
    color:str = Field(default="#FFFFFF", description="カテゴリの色を表す16進カラーコード", unique=True)
    transactions: list["Transaction"] = Relationship(back_populates="category")
