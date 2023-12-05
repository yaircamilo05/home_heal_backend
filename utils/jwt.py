import datetime
import os
import time
#from jwt import encode, decode
from jwt import DecodeError, ExpiredSignatureError
from schemas.user import User, UserGetLogin, UserWithMenus

def create_token(user: UserGetLogin) -> str:
    # key_hash = os.environ.get('KEY_HASH_TOKEN')
    # token: str = encode(
    #     payload=user.model_dump(),
    #     key=key_hash, algorithm='HS256'
    # )
    # return token
    return user.model_dump()

def create_token_email(user: UserGetLogin) -> str:
    payload = user.model_dump()
    key_hash = os.environ.get('KEY_HASH_TOKEN')
    payload['exp'] = int(time.mktime((datetime.datetime.now() + datetime.timedelta(minutes=5)).timetuple()))
    # token: str = encode(
    #     payload=payload,
    #     key=key_hash, 
    #     algorithm='HS256'
    # )
    return payload

def validate_token(token: str) -> dict:
    key_hash = os.environ.get('KEY_HASH_TOKEN')
    try:
        # data: dict = decode(token, key_hash, algorithms=['HS256'])
        return token
    except DecodeError:
        return None
    except ExpiredSignatureError:
        return None

def validate_token_email(token: str):
    key_hash = os.environ.get('KEY_HASH_TOKEN')
    try:
        # data: dict = decode(token, key_hash, algorithms=['HS256'])
        return token
    except DecodeError:
        return -1
    except ExpiredSignatureError:
        return -2