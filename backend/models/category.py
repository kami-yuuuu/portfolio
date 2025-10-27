from sqlmodel import Field, SQLModel
from typing import Optional,List, TYPE_CHECKING, Annotated
from sqlmodel import Relationship, func, Column, DateTime
from datetime import datetime
from pydantic import BeforeValidator

#循環参照を避けて型ヒントを提供するための条件付きインポート
if TYPE_CHECKING:
    from .transaction import Transaction


class BaseCategory(SQLModel):
    """
    取引カテゴリの基本モデル
    取引カテゴリに共通する属性を定義する

    Attributes:
        name (str): カテゴリの名前
        type (str): 取引の分類（収入/支出など）
        color (str): カテゴリの色を表す16進カラーコード
    """

    name: str = Field(description="カテゴリの名前", unique=True)
    type: str = Field(description="取引の分類（収入/支出など）")
    color: str = Field(default="#FFFFFF", description="カテゴリの色を表す16進カラーコード", unique=True)


class Category(BaseCategory, table=True):
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
    transactions: List['Transaction'] = Relationship(back_populates="category")
    created_at: Optional[datetime] = Field(default=None, description="作成日時", sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(default=None, description="更新日時", sa_column=Column(DateTime(timezone=True), onupdate=func.now()))



# validatorを使用してtypeフィールドの値が特定の値であることを保証
def validate_category_type(value: str) -> str:
    allowed_types = {"income", "expense", "transfer"}
    if value.lower() not in allowed_types:
        raise ValueError(f"Invalid category type: {value}. Allowed types are: {allowed_types}")
    return value.lower()

class CategoryCreate(BaseCategory):
    """
    取引カテゴリ作成用モデル
    新しい取引カテゴリを作成するためのデータ構造を定義する

    Attributes:
        name (str): カテゴリの名前
        type (str): 取引の分類（収入/支出など）を表す。"income", "expense", "transfer"のいずれか
        color (str): カテゴリの色を表す16進カラーコード
    """

    name: str = Field(description="カテゴリの名前")
    type : Annotated[str, BeforeValidator(validate_category_type)] = Field(description="取引の分類（収入/支出など）")
    color: str = Field(default="#FFFFFF", description="カテゴリの色を表す16進カラーコード")

class CategoryRead(BaseCategory):
    """
    取引カテゴリ読み取り用モデル
    取引カテゴリの情報を取得するためのデータ構造を定義する

    Attributes:
        id (int): カテゴリの一意の識別子
        name (str): カテゴリの名前
        type (str): 取引の分類（収入/支出など）
        color (str): カテゴリの色を表す16進カラーコード
        created_at (Optional[datetime]): 作成日時
        updated_at (Optional[datetime]): 更新日時
    """

    id: int = Field(description="カテゴリの一意の識別子")
    name: str = Field(description="カテゴリの名前")
    type: str = Field(description="取引の分類（収入/支出など）")
    color: str = Field(default="#FFFFFF", description="カテゴリの色を表す16進カラーコード")
    transactions: List['Transaction'] = Relationship(back_populates="category")
    created_at: Optional[datetime] = Field(default=None, description="作成日時")
