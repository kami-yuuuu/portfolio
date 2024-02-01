from fastapi import APIRouter, Depends, HTTPException, Response, Request, status, Query, Path, Cookie, Body
from fastapi.encoders import jsonable_encoder
from ..schema import Todo, TodoBody, SuccessMsg
from typing import List
from ..database import db_create_todo, db_get_all_todo, db_get_single_todo, db_update_todo, db_delete_todo

router = APIRouter()


@router.post('/api/todo', response_model=Todo)
async def create_todo(request: Request, Response: Response, data: TodoBody):
    todo = jsonable_encoder(data)
    res = await db_create_todo(todo)
    if res:
        Response.status_code = status.HTTP_201_CREATED
        return res
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='create task failed')


@router.get('/api/todo', response_model=List[Todo])
async def get_todo_list():
    res = await db_get_all_todo()
    return res


@router.get('/api/todo/{id}', response_model=Todo)
async def get_single_todo(id: str = Path(..., min_length=24, max_length=24)):
    res = await db_get_single_todo(id)
    if res:
        return res
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'task of {id} does not found')


@router.put('/api/todo/{id}', response_model=Todo)
async def update_todo(request: Request, response: Response,  id: str = Path(..., min_length=24, max_length=24), data: TodoBody = Body()):
    todo = jsonable_encoder(data)
    res = await db_update_todo(id, todo)
    if res:
        return res
    raise HTTPException(status_code=status.HTTP, detail=f'task of {id} does not found')


@router.delete('/api/todo/{id}', response_model=SuccessMsg)
async def delete_todo(request: Request, response: Response, id: str = Path(..., min_length=24, max_length=24)):
    res = await db_delete_todo(id)
    if res:
        return {'message': f'task of {id} has been deleted successfully'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'delete task of {id} failed')

