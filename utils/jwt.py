import datetime
import os
import time
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from schemas.user import User, UserWithMenus

def create_token(user: User) -> str:
    token: str = encode(
        payload=user.model_dump(),
        key='iBObRG5saVjUOKj'
    )
    return token

def create_token_email(user: User) -> str:
    payload = user.model_dump()
    key_hash = os.environ.get('KEY_HASH_TOKEN')
    payload['exp'] = int(time.mktime((datetime.datetime.now() + datetime.timedelta(minutes=2)).timetuple()))
    token: str = encode(
        payload=payload,
        key=key_hash, 
        algorithm='HS256'
    )
    return token

def validate_token(token: str) -> dict:
    try:
        data: dict = decode(token, 'iBObRG5saVjUOKj', algorithms=['HS256'])
        return data
    except DecodeError:
        return None
    except ExpiredSignatureError:
        return None
