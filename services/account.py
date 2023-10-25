from models.base import User
from utils import auth, jwt
from schemas.login import credentials_login


def login(credentials:credentials_login, db) -> str:
    passaword_encript = auth.encript_password(credentials.password)
    if not exit_user(credentials.email, passaword_encript, db):
        return None
    user = get_user_by_email_and_password(credentials.email, passaword_encript, db)
    token = jwt.create_token(user)
    return token
def validate_token(token: str) -> dict:
    data_token: dict = jwt.validate_token(token)
    return data_token


def exit_user(email: str, password: str, db) -> bool:
    user = get_user_by_email_and_password(email, password, db)
    return user != None

def get_user_by_email_and_password(email: str, password: str, db) -> User:
    user = db.query(User).filter(User.email == email & User.password == password).first()
    return user;