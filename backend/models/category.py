from sqlmodel import Field, SQLModel, String, create_engine


class Category(SQLModel, table=True):
    id:int | None = Field(nullable=False, primary_key=True)
    name:str
    type:str
    color:str







