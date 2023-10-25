from models.rol import Rol
from schemas.rol import RolCreate


def create_rol(new_rol: RolCreate, db):
    rol = Rol(name=new_rol.name)
    db.add(rol)
    db.commit()
    db.refresh(rol)

    return rol

def exist_rol(id: int, db):
    rol = db.query(Rol).filter(Rol.id == id).first()
    if rol is None:
        return False
    return True

def all_roles(db):
    return db.query(Rol).all()