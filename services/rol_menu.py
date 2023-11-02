from sqlalchemy.orm import Session
from models.base import Rol, Menu, rol_menu
from sqlalchemy import select


def add_rol_menu(db: Session, rol_id: int, menu_id: int):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    exit_munu = exist_rol_menu(db, rol_id, menu_id)

    if exit_munu:
        return None
    
    if rol and menu:
        rol.menus.append(menu)
        db.commit()
        db.refresh(rol)
    else:
        return None
    return rol.menus

#funcion para validar si un rol tiene ya un menu
def exist_rol_menu(db: Session, rol_id: int, menu_id: int):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    menu_exit = None
    for menu in rol.menus:
        if menu.id == menu_id:
            menu_exit = menu
    if menu_exit is not None:
        return True
    return False
    

def remove_rol_menu(db: Session, rol_id: int, menu_id: int) -> bool:
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if rol and menu:
        rol.menus.remove(menu)
        db.commit()
        return True
    return False

def get_menus_role(db: Session, role_id: int):
    stmt = select(Menu).join(rol_menu).join(Rol).where(Rol.id == role_id)
    menus = db.execute(stmt).scalars().all()
    return menus

