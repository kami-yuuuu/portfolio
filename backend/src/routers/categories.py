from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List

from models.category import Category, CategoryCreate, CategoryUpdate, CategoryRead
from dependencies import get_session
from database_errors import commit_or_conflict

router = APIRouter()


@router.get("/", response_model=List[CategoryRead])
def read_categories(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Category).offset(skip).limit(limit)).all()


@router.get("/{category_id}", response_model=CategoryRead)
def read_category(category_id: int, session: Session = Depends(get_session)):
    if category_id <= 0:
        raise HTTPException(status_code=422, detail="category_id must be greater than zero")
    category = session.get(Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(category: CategoryCreate, session: Session = Depends(get_session)):
    db_category = Category.model_validate(category)
    session.add(db_category)
    commit_or_conflict(session)
    session.refresh(db_category)
    return db_category


@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, category_update: CategoryUpdate, session: Session = Depends(get_session)):
    if category_id <= 0:
        raise HTTPException(status_code=422, detail="category_id must be greater than zero")
    db_category = session.get(Category, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category_update.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)
    session.add(db_category)
    commit_or_conflict(session)
    session.refresh(db_category)
    return db_category


@router.delete("/{category_id}", response_model=dict[str, bool])
def delete_category(category_id: int, session: Session = Depends(get_session)):
    if category_id <= 0:
        raise HTTPException(status_code=422, detail="category_id must be greater than zero")
    category = session.get(Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    commit_or_conflict(session)
    return {"ok": True}
