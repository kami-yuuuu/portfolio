from sqlmodel import Field, SQLModel, Relationship, Column, DateTime, func
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .transaction import Transaction


class Category(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    name:str = Field(description="カテゴリの名前", unique=True)
    type: str = Field(description="取引の分類（収入/支出など）")
    color:str = Field(default="#FFFFFF", description="カテゴリの色を表す16進カラーコード", unique=True)
    transactions: list["Transaction"] = Relationship(back_populates="category")
    created_at: Optional[str] = Field(default=None, description="作成日時", sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[str] = Field(default=None, description="更新日時", sa_column=Column(DateTime(timezone=True), onupdate=func.now()))
