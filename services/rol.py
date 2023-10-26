from models.base import Rol
from schemas.rol import RolSchema


# Post rol


def post_rol(arg_rol: RolSchema, db):
    exist = exist_rol(arg_rol.name, db)
    if exist:
        return None
    rol = Rol(**arg_rol.model_dump())
    db.add(rol)
    db.commit()
    db.refresh(rol)

    return rol

# Get rol


def get_roles(db) -> list[Rol]:
    return db.query(Rol).all()


def get_role(id: int, db) -> Rol:
    return db.query(Rol).filter(Rol.id == id).first()


def exist_rol(id: int, db) -> bool:
    rol = db.query(Rol).filter(Rol.id == id).first()
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