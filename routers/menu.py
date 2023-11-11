
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.menu import MenuSchema, MenuOut
from services.menu import post_menu, get_menus, get_menu, put_menu, delete_menu
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/create_menu", response_model=MenuOut)
def create_menu(menu: MenuSchema, db: Session = Depends(get_db)):
    menuCreated=  post_menu(db, menu)
    if menuCreated is None:
        raise HTTPException(status_code=404, detail="Error creating menu")
    return JSONResponse(status_code=201, content=jsonable_encoder({"data": menuCreated}))


@router.get("/menus", response_model=List[MenuOut])
def read_menus(db: Session = Depends(get_db)):
    db_menus = get_menus(db)
    if db_menus is None:
        raise HTTPException(status_code=404, detail="Menus not found")
    return JSONResponse(status_code=200, content=jsonable_encoder({"data": db_menus}))


@router.get("/get_menu_by_id/{menu_id}", response_model=MenuOut)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return JSONResponse(status_code=200, content=jsonable_encoder({"data": db_menu}))


@router.put("/edit_menu/{menu_id}", response_model=MenuOut)
def update_menu(menu_id: int, menu: MenuSchema, db: Session = Depends(get_db)):
    db_menu = put_menu(db, menu_id=menu_id, menu=menu)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return JSONResponse(status_code=200, content=jsonable_encoder({"data": db_menu}))



@router.delete("/delete_menu/{menu_id}", response_model=MenuOut)
def delete_menu_route(menu_id: int, db: Session = Depends(get_db)):
    menu_removed = delete_menu(db, menu_id=menu_id)
    if menu_removed is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'data': False}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': True}
    )
