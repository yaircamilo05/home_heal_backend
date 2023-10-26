from jwt import encode, decode
from jwt import DecodeError, ExpiredSignatureError
from schemas.user import User, UserWithMenus

def create_token(user: User) -> str:
    token: str = encode(
        payload=user.model_dump(),
        key='iBObRG5saVjUOKj', algorithm='HS256'
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
