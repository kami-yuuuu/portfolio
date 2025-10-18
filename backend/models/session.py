from sqlmodel import SQLModel, create_engine
from .category import Category
import os


postgres_url:str =os.getenv("DATABASE_URL",default="postgresql://postgres::password@db:5432/postgresdb")

engine = create_engine(postgres_url, echo=True)

SQLModel.metadata.create_all(engine)

