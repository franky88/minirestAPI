import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from server.models.auth import Token
from server.config.database import user_col
from server.schemas.users_schemas import user_list_serializer
from bson import ObjectId

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALOGORITHM = "HS256"

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    print("user", user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not authenticate user")
    token = create_access_token(user['username'], user['id'], timedelta(minutes=30))
    return {
        'access_token': token,
        "token_type": "bearer"
    }


def authenticate_user(username: str, password: str):
    user = user_list_serializer(user_col.find({"username": username}))[0]
    print("auth user", user)
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user

def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALOGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALOGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not authenticate user")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not authenticate user")