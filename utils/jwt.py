from jwt import encode, decode
from schemas.login import credentials_login
from schemas.user import User

def create_token(user: User) -> str:
    token: str = encode(payload=user.model_dump(), key="iBObRG5saVjUOKj", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key="iBObRG5saVjUOKj", algorithms=['HS256'])
    return data