from fastapi.encoders import jsonable_encoder
from models.base import Rol
from schemas.rol import RolOut, RolSchema, RolWithMenus
from services.rol_menu import get_menus_role


# Post rol


def post_rol(arg_rol: RolSchema, db):
    exist = exist_rol(arg_rol.name, db)
    if exist:
        return None
    rol = Rol(**arg_rol.model_dump())
    db.add(rol)
    db.commit()
    db.refresh(rol)

    return RolOut(**rol.__dict__) 

# Get rol


def get_roles(db) -> list[Rol]:
    return db.query(Rol).all()

def get_roles_with_menus(db) -> list[RolWithMenus]:
    roles_with_menus:RolWithMenus = []
    roles = db.query(Rol).all()
    for rol in roles:
        menus_rol = get_menus_role(db, rol.id)
        rol_dict = rol.__dict__
        rol_dict['menus'] = jsonable_encoder(menus_rol)
        rol_with_menus = RolWithMenus(**rol_dict)
        roles_with_menus.append(rol_with_menus)
    return roles_with_menus


def get_role(id: int, db) -> Rol:
    return db.query(Rol).filter(Rol.id == id).first()


def exist_rol(name: str, db) -> bool:
    rol = db.query(Rol).filter(Rol.name == name).first()
    return rol

# Update rol


def put_rol(id: int, rol: RolSchema, db) -> Rol:
    if not exist_rol(id, db):
        return None
    db.query(Rol).filter(Rol.id == id).update(rol.model_dump())
    db.commit()
    return rol

# Delete rol

def delete_rol(id: int, db) -> int:
    if not exist_rol(id, db):
        return None
    db.query(Rol).filter(Rol.id == id).delete()
    db.commit()
    return id