from sqlalchemy.orm import Session
from models.base import Rol
from schemas.rol import RolOut, RolCreate, RolUpdate
from typing import List

# Post rol


def post_rol(rol: RolCreate, database: Session) -> RolOut:
    if exist_rol_name(rol.name, database):
        return None
    db_rol: Rol = Rol(**rol.model_dump())
    database.add(db_rol)
    database.commit()
    database.refresh(db_rol)

    return RolOut(**db_rol.__dict__)

# Get rol


def get_roles(database) -> List[RolOut]:
    db_roles: List[Rol] = database.query(Rol).all()
    return [RolOut(**rol.__dict__) for rol in db_roles]


def get_role(id: int, database: Session) -> RolOut:
    if not exist_rol_id(id, database):
        return None
    db_rol: Rol = database.query(Rol).filter(Rol.id == id).first()
    return RolOut(**db_rol.__dict__) if db_rol else None


def exist_rol(name: str, db) -> bool:
    db_rol = db.query(Rol).filter(Rol.name == name).first()
    return RolOut(**db_rol.__dict__) if db_rol else None

# Update rol


def put_rol(id: int, db_rol: RolUpdate, database: Session) -> RolOut:
    db_rol: Rol = database.query(Rol).filter(Rol.id == id).first()
    if db_rol is None:
        return None

    for attr, value in db_rol.model_dump().items():
        setattr(db_rol, attr, value)

    database.commit()
    database.refresh(db_rol)
    return RolOut(**db_rol.__dict__)

# Delete rol


def delete_rol(id: int, database: Session) -> bool:
    db_rol: Rol = database.query(Rol).filter(Rol.id == id).first()
    if db_rol is None:
        return False
    database.delete(db_rol)
    database.commit()
    return True

# Utils


def exist_rol_name(name: str, database: Session) -> bool:
    db_rol: Rol = database.query(Rol).filter(Rol.name == name).first()
    return False if db_rol is None else True


def exist_rol_id(id: int, database: Session) -> bool:
    db_rol: Rol = database.query(Rol).filter(Rol.id == id).first()
    return False if db_rol is None else True
