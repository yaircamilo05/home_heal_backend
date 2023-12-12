import datetime
import os
import time
from jose import jwt
from schemas.user import UserGetLogin

def create_token(user: UserGetLogin) -> str:
    key_hash = os.environ.get('KEY_HASH_TOKEN')
    token: str = jwt.encode(
        claims=user.model_dump(),
        key=key_hash, 
        algorithm='HS256'
    )
    return token

def create_token_email(user: UserGetLogin) -> str:
    payload = user.model_dump()
    key_hash = os.environ.get('KEY_HASH_TOKEN')
    payload['exp'] = int(time.mktime((datetime.datetime.now() + datetime.timedelta(minutes=3)).timetuple()))
    token: str = jwt.encode(
        claims=payload,
        key=key_hash, 
        algorithm='HS256'
    )
    return token

def validate_token(token: str) -> dict:
    key_hash = os.environ.get('KEY_HASH_TOKEN')
    print("La clave para el token",key_hash)
    try:
        data: dict = jwt.decode(
            token=token, 
            key=key_hash, 
            algorithms=['HS256']
        )
        return data
    except jwt.JWTError:
        return None
    except jwt.ExpiredSignatureError:
        return None

def validate_token_email(token: str):
    key_hash = os.environ.get('KEY_HASH_TOKEN')
    try:
        data: dict = jwt.decode(
            token=token, 
            key=key_hash, 
            algorithms=['HS256']
        )
        return data
    except jwt.JWTError:
        return -1
    except jwt.ExpiredSignatureError:
        return -2