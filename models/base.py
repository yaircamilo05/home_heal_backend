from typing import Optional
from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base


rol_menus = Table(
    'rol_menus', Base.metadata,
    Column('menu_id', ForeignKey('menus.id'), primary_key=True),
    Column('rol_id', ForeignKey('roles.id'), primary_key=True),
)

DoctorPatients = Table(
    'doctor_patients', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('doctor_id', ForeignKey('doctors.id')),
    Column('patient_id', ForeignKey('patients.id')),
)


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String)
    icon = Column(String)
    link = Column(String)
    roles = relationship('Rol', secondary=rol_menus, back_populates='menus')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    lastname = Column(String(100))
    image_url = Column(String(255), nullable=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))

    rol_id = Column(Integer, ForeignKey('roles.id'))
    rol = relationship('Rol', back_populates='users')


class Rol(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    description = Column(String(255))

    users = relationship('User', back_populates='rol')
    menus = relationship('Menu', secondary=rol_menus, back_populates='roles')



class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True, autoincrement=True)

    gender = Column(String(1))
    birthdate = Column(Date)
    description = Column(String(255))
    address = Column(String(255))

    user_id = Column(Integer, ForeignKey('users.id'))
    familiar_user_id = Column(Integer, ForeignKey('users.id'))

    doctors = relationship('Doctor', secondary=DoctorPatients, back_populates='patients')
    vital_signs = relationship('VitalSign', back_populates='patient', uselist=False)
    vital_sign_records = relationship('VitalSignRecord', back_populates='patient')
    diagnostics = relationship('Diagnostic', back_populates='patient')


class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    speciality = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id'))
    patients = relationship('Patient', secondary=DoctorPatients, back_populates='doctors')


class VitalSign(Base):
    __tablename__ = 'vital_signs'
    id = Column(Integer, primary_key=True, autoincrement=True)

    hearth_rate = Column(Integer)
    blood_pressure = Column(Integer)
    O2_saturation = Column(Integer)

    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient', back_populates='vital_signs')


class VitalSignRecord(Base):
    __tablename__ = 'vital_sign_records'
    id = Column(Integer, primary_key=True, autoincrement=True)

    hearth_rate = Column(Integer)
    blood_pressure = Column(Integer)
    O2_saturation = Column(Integer)

    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient', back_populates='vital_sign_records')


class Cares(Base):
    __tablename__ = 'cares'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255))
    doctor_patients_id = Column(Integer, ForeignKey('doctor_patients.id'))



class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True, autoincrement=True)

    reason = Column(String(255))
    date = Column(Date)
    state = Column(String(15))

    doctor_patients_id = Column(Integer, ForeignKey('doctor_patients.id'))
    


class Diagnostic(Base):
    __tablename__ = 'diagnostics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255))

    doctor_patients_id = Column(Integer, ForeignKey('doctor_patients.id'))
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient', back_populates='diagnostics')
