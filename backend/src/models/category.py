from typing import List, Optional, TYPE_CHECKING, Literal
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, DateTime, func

if TYPE_CHECKING:
    from .transaction import Transaction


class BaseCategory(SQLModel):
    name: str = Field(min_length=1, max_length=100, description="カテゴリの名前")
    type: Literal["income", "expense"] = Field(description="取引の分類")
    color: str = Field(default="#FFFFFF", pattern=r"^#[0-9A-Fa-f]{6}$", description="16進カラーコード")


class Category(BaseCategory, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, min_length=1, max_length=100)
    transactions: List['Transaction'] = Relationship(back_populates="category")
    created_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), onupdate=func.now()))


class CategoryCreate(BaseCategory):
    pass


class CategoryUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    type: Optional[Literal["income", "expense"]] = None
    color: Optional[str] = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")


class CategoryRead(SQLModel):
    id: int
    name: str
    type: str
    color: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
