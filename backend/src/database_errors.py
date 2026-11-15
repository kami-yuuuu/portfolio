from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlmodel import Session


def commit_or_conflict(session: Session) -> None:
    """Commit a write and turn database constraint violations into a safe 409."""
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="The request conflicts with existing data or referenced records.",
        ) from exc
