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

    roles = relationship('Rol', back_populates='users')
    diagnoses = relationship(
        'Diagnosis', secondary='diagnoses_users', back_populates='users'
    )


class Rol(Base):

    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    description = Column(String(255))

    users = relationship('User', back_populates='roles')


class Diagnosis(Base):

    __tablename__ = 'diagnoses'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255))
    date = Date()

    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(
        'User', secondary='diagnoses_users',
        back_populates='diagnoses'
    )


class DiagnosesUser(Base):

    __tablename__ = 'diagnoses_users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    diagnosis_id = Column(Integer, ForeignKey('diagnoses.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
