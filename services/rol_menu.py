from sqlalchemy.orm import Session
from models.base import Rol, Menu

async def add_rol_to_menu(db: Session, rol_id: int, menu_id: int) -> bool:
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if rol and menu:
        rol.menus.append(menu)
        db.commit()
        return True
    return False

async def remove_rol_from_menu(db: Session, rol_id: int, menu_id: int) -> bool:
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if rol and menu:
        rol.menus.remove(menu)
        db.commit()
        return True
    return False