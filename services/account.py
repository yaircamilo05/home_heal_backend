from models.base import User
from schemas.user import User as UserGet
from utils import auth, jwt
from schemas.login import credentials_login


def login(credentials:credentials_login, db) -> str:
    if not exit_user(credentials.email, db):
        return None
    user = get_user_by_email(credentials.email, db)
    if user and auth.check_password(credentials.password, user.password):
        user_get = UserGet(**user.__dict__)
        token = jwt.create_token(user_get)
    return token
def validate_token(token: str) -> dict:
    data_token = jwt.validate_token(token)
    if not data_token:
        return None 
    return data_token

def exit_user(email: str, db) -> bool:
    user = get_user_by_email(email, db)
    return user != None

def get_user_by_email(email: str, db) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user