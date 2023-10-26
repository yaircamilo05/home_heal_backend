from sqlalchemy.orm import Session
from models.base import Menu
from schemas.menu import MenuSchema
from typing import List


def exist_menu(db: Session, menu_title: str) -> bool:
    menu = db.query(Menu).filter(Menu.title == menu_title).first()
    return menu


def post_menu(db: Session, menu: MenuSchema) -> Menu:
    if exist_menu(db, menu.title):
        return None
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def get_menus(db: Session) -> List[Menu]:
    return db.query(Menu).all()


def get_menu(db: Session, menu_id: int) -> Menu:
    return db.query(Menu).filter(Menu.id == menu_id).first()


def put_menu(db: Session, menu_id: int, menu: MenuSchema) -> Menu:
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu:
        for key, value in menu.dict().items():
            setattr(db_menu, key, value)
        db.commit()
        db.refresh(db_menu)
    return db_menu


def delete_menu(db: Session, menu_id: int) -> Menu:
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
    return db_menu
