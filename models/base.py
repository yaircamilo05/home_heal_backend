from typing import Optional
from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base


rol_menu = Table(
    'rol_menu', Base.metadata,
    Column('menu_id', ForeignKey('menus.id'), primary_key=True),
    Column('rol_id', ForeignKey('roles.id'), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    lastname = Column(String(100))
    file_img = Column(String(255), nullable=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    rol_id = Column(Integer, ForeignKey('roles.id'))

    rol = relationship('Rol', back_populates='users')


class Rol(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    description = Column(String(255))

    users = relationship('User', back_populates='rol')
    menus = relationship(
        'Menu', secondary=rol_menu, back_populates='roles'
    )


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    icon = Column(String)
    link = Column(String)
    roles = relationship(
        'Rol', secondary=rol_menu, back_populates='menus'
    )
