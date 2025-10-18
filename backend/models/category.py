from sqlmodel import Field, SQLModel, String, create_engine


class Category(SQLModel, table=True):
    id:int | None = Field(nullable=False, primary_key=True)
    name:str
    type: str = Field(description="取引の分類（収入/支出など）")
    color:str = Field(default="#FFFFFF", description="カテゴリの色を表す16進カラーコード", unique=True)

