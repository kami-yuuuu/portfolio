from sqlmodel import Session
from models.session import engine

async def get_session():
    with Session(engine) as session:
        yield session
