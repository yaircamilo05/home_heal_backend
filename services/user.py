from schemas.user import UserCreate
from models.user import User

def create_user(new_user: UserCreate, db):
    exist = exist_user(new_user.email, db)
    if exist:
        return None
    usr = User(**new_user.model_dump())
    ## Acá va la logica de consulta en la base de datos
    db.add(usr)
    db.commit()
    db.refresh(usr)
    return usr

def exist_user(email: str, db):
    usr = db.query(User).filter(User.email == email).first()
    return usr

def all_users(db):
    return db.query(User).all()

