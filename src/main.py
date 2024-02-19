from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .routers import route_todo, route_auth
from .schema import SuccessMsg, Token, User, UserBody, CsrfSettings, UserResponse, TokenData
from .database import db_signup
from decouple import config
from typing import Annotated
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from .routers.route_auth import get_current_user

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES')

app = FastAPI(docs_url='/docs')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app.include_router(route_todo.router)
app.include_router(route_auth.router)

origins = [
    'http://localhost:3000',
    'localhost:3000',
    'http://localhost:5173',
    'localhost:5173',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.exception_handler(CsrfProtectError)
async def csrf_protect_error_handler(request: Request, exc) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.message}
    )


#def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
#    to_encode = data.copy()
#    if expires_delta:
#        expire = datetime.utcnow() + expires_delta
#    else:
#        expire = datetime.utcnow() + timedelta(minutes=15)
#    to_encode.update({'exp': expire})
#    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#    return encoded_jwt
#
#
#async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
#    credentials_exception = HTTPException(
#        status_code=status.HTTP_401_UNAUTHORIZED,
#        detail='Could not validate credentials',
#        headers={'WWW-Authenticate': 'Bearer'},
#    )
#    try:
#        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#        username: str = payload.get('sub')
#        if username is None:
#            raise credentials_exception
#        token_data = TokenData(username=username)
#    except JWTError:
#        raise credentials_exception
#    user = await db_getuser(token_data.username)
#    if user is None:
#        raise credentials_exception
#    return UserResponse(id=user['id'], username=user['username'], email=user['email'])


@app.get('/', response_model=SuccessMsg)
async def root():
    return {'message': 'Welcome to Fast API'}


#@app.post('/token', response_model=Token)
#async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#    form_data = jsonable_encoder(form_data)
#    user = await db_login(form_data)
#    if not user:
#        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')
#    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
#    access_token = create_access_token(data={'sub': user['username'], 'id': user['id']},
#                                       expires_delta=access_token_expires)
#    return Token(access_token=access_token, token_type='bearer')


@app.post('/signup', response_model=UserResponse)
async def signup(request: Request, user: Annotated[UserBody, Depends()], csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)
    user = jsonable_encoder(user)
    new_user = await db_signup(user)
    if new_user:
        return UserResponse(id=new_user['id'], username=new_user['username'], email=new_user['email'])
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Signup failed')


@app.get('/user/me', response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


