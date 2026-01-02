from sqlmodel import SQLModel, create_engine
from . import category, transaction, payment_method
from sys import argv
import os



postgres_url:str =os.getenv("DATABASE_URL",default="postgresql://postgres:password@db:5432/postgresdb")



engine = create_engine(postgres_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def delete_db_and_tables():
    SQLModel.metadata.drop_all(engine)




if __name__ == "__main__":  
    if "create" in argv:
        create_db_and_tables()
    elif "delete" in argv:
        delete_db_and_tables()
    else:
        print("Usage: python session.py [create|delete]")

