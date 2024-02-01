from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from typing import Union
from bson.objectid import ObjectId
from passlib.context import CryptContext

mongodb_api_key = config('MONGO_DB_API_KEY')
client = AsyncIOMotorClient(mongodb_api_key)

database = client.API_DB
user_collection = database.user
todo_collection = database.todo

crypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def todo_serializer(todo) -> dict:
    return {
        'id': str(todo['_id']),
        'title': todo['title'],
        'description': todo['description']
    }


def user_serializer(user) -> dict:
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
    }


async def db_create_todo(data: dict) -> Union[dict, bool]:
    todo = await todo_collection.insert_one(data)
    new_todo = await todo_collection.find_one({'_id': todo.inserted_id})
    return todo_serializer(new_todo) if new_todo else False


async def db_get_all_todo() -> list:
    todos = []
    for todo in await todo_collection.find().to_list(length=100):
        todos.append(todo_serializer(todo))
    return todos


async def db_get_single_todo(id: str) -> Union[dict, bool]:
    todo = await todo_collection.find_one({'_id': ObjectId(id)})
    return todo_serializer(todo) if todo else False


async def db_update_todo(id: str, data: dict) -> Union[dict, bool]:
    todo = todo_collection.find_one({'_id': ObjectId(id)})
    if todo:
        result = await todo_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.modified_count >= 1:
            new_todo = await todo_collection.find_one({'_id': ObjectId(id)})
            return todo_serializer(new_todo) if new_todo else False
    return False


async def db_delete_todo(id: str) -> bool:
    todo = await todo_collection.find_one({'_id': ObjectId(id)})
    if todo:
        result = await todo_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count >= 1:
            return True
    return False


async def db_signup(data) -> dict:
    username = data['username']
    email = data['email']
    password = data['password']
    overlap_user = await user_collection.find_one({'username': username})
    if overlap_user:
        raise HTTPException(status_code=400, detail='username is already registered')
    overlap_email = await user_collection.find_one({'email': email})
    if overlap_email:
        raise HTTPException(status_code=400, detail='Email is already registered')
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail='password is invalid')
    hashed_password = crypt_context.hash(password)
    user = await user_collection.insert_one({'username': username, 'email': email, 'password': hashed_password})
    new_user = await user_collection.find_one({'_id': user.inserted_id})
    return user_serializer(new_user) if new_user else False


async def db_login(data) -> dict:
    username = data['username']
    password = data['password']
    user = await user_collection.find_one({'username': username})
    if not user or not crypt_context.verify(password, user['password']):
        raise HTTPException(status_code=400, detail='username or password is invalid')
    return user_serializer(user)


async def db_getuser(username: str) -> Union[dict, None]:
    user = await user_collection.find_one({'username': username})
    return user_serializer(user) if user else None
