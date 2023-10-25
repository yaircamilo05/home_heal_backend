from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    lastname = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    rol_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Rol', back_populates='users')


class Rol(Base):

    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    description = Column(String(255))

    users = relationship('User', back_populates='roles')
    menus = relationship('MenusRol', back_populates='rol')


class Menus(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(127))
    icon = Column(String(127))

    roles = relationship('MenusRol', back_populates='menu')


class MenusRol(Base):
    __tablename__ = 'menus_roles'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    rol_id = Column(Integer, ForeignKey('roles.id'))

    menu = relationship('Menus', back_populates='roles')
    rol = relationship('Rol', back_populates='menus')
