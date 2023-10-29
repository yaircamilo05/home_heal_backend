from sqlalchemy.orm import Session
from models.base import Rol
from schemas.rol import RolCreate, RolUpdate, RolSchema
from typing import List


# Post rol


def post_rol(rol: RolCreate, database: Session) -> RolSchema:
    new_rol: Rol = Rol(**rol.model_dump())
    database.add(new_rol)
    database.commit()
    database.refresh(new_rol)

    return RolSchema(**new_rol.__dict__)

# Get rol


def get_roles(database) -> List[RolSchema]:
    roles: List[Rol] = database.query(Rol).all()
    return [RolSchema(**role.__dict__) for role in roles]


def get_role(id: int, database: Session) -> RolSchema:
    rol: Rol = database.query(Rol).filter(Rol.id == id).first()
    return RolSchema(**rol.__dict__) if rol else None


# Update rol


def put_rol(id: int, rol: RolUpdate, database: Session) -> RolSchema:
    rol_obj: Rol = database.query(Rol).filter(Rol.id == id).first()

    if rol_obj is None:
        return None
    for attr, value in rol.model_dump().items():
        setattr(rol_obj, attr, value)

    database.commit()
    database.refresh(rol_obj)
    return RolSchema(**rol_obj.__dict__)

# Delete rol


def delete_rol(id: int, database: Session) -> RolSchema:
    rol_obj: Rol = database.query(Rol).filter(Rol.id == id).first()
    if rol_obj is None:
        return None
    database.delete(rol_obj)
    database.commit()
    return RolSchema(**rol_obj.__dict__)

# Utils


def exist_rol_name(name: str, database: Session) -> bool:
    rol: Rol = database.query(Rol).filter(Rol.name == name).first()
    return False if rol is None else True


def exist_rol_id(id: int, database: Session) -> bool:
    rol: Rol = database.query(Rol).filter(Rol.id == id).first()
    return False if rol is None else True
