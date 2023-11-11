from fastapi.encoders import jsonable_encoder
from models.base import Rol
from sqlalchemy.orm import Session
from schemas.rol import RolCreate, RolUpdate, RolOut


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


def get_roles(db) -> list[Rol]:
    return db.query(Rol).all()

# def get_roles_with_menus(db) -> list[RolWithMenus]:
#     roles_with_menus:RolWithMenus = []
#     roles = db.query(Rol).all()
#     for rol in roles:
#         menus_rol = get_menus_role(db, rol.id)
#         rol_dict = rol.__dict__
#         rol_dict['menus'] = jsonable_encoder(menus_rol)
#         rol_with_menus = RolWithMenus(**rol_dict)
#         roles_with_menus.append(rol_with_menus)
#     return roles_with_menus


def get_role(id: int, database: Session) -> RolOut:
    if not exist_rol_id(id, database):
        return None
    db_rol: Rol = database.query(Rol).filter(Rol.id == id).first()
    return RolOut(**db_rol.__dict__) if db_rol else None


def exist_rol(name: str, db) -> bool:
    db_rol = db.query(Rol).filter(Rol.name == name).first()
    return RolOut(**db_rol.__dict__) if db_rol else None

# Update rol


def put_rol(id: int, rol: RolUpdate, database: Session) -> RolOut:
    db_rol: Rol = database.query(Rol).filter(Rol.id == id).first()
    if db_rol is None:
        return None

    for attr, value in rol.model_dump().items():
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
