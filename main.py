import os
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
from middlewares.error import ErrorHandler
from database.db import Base, engine
from middlewares.guard import SuperAdmin
from routers import user, rol, account, menu, rol_menu, file, query, patient, vital_signs,appointment,email, doctor, cares, diagnostic

import uvicorn


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.title = "Home Heal API"
app.version = "1.0"

# Adicion de middlewares
app.add_middleware(ErrorHandler)
origins = ["*"]
app.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

# se deben agregar las variables de entorno del servidor de la base de datos y las api keys de los servicios de terceros

# Adición de routers
app.include_router(account.router, tags=["Accounts"], prefix="/account")
app.include_router(appointment.router, tags=["Appointments"], prefix="/appointment")
app.include_router(cares.router, tags=["Cares"], prefix="/cares")
app.include_router(diagnostic.router, tags=["Diagnostic"], prefix="/diagnostic")
app.include_router(doctor.router, tags=["Doctors"], prefix="/doctor")
app.include_router(doctor.router, tags=["Doctors"], prefix="/doctor")
app.include_router(email.router, tags=["Emails"], prefix="/email")
app.include_router(file.router, tags=["Files"], prefix="/file")
app.include_router(menu.router, tags=["Menus"], prefix="/menu")
app.include_router(patient.router, tags=["Patients"], prefix="/patient")
app.include_router(query.router, tags=["Queries"], prefix="/query")
app.include_router(rol.router, tags=["Roles"], prefix="/rol")
app.include_router(rol_menu.router, tags=["RolesMenus"], prefix="/rol_menu", dependencies=[ Depends(SuperAdmin())])
app.include_router(user.router, tags=["Users"], prefix="/user")
app.include_router(vital_signs.router, tags=["Vitals Signs"], prefix="/vitalsigns")
# app.include_router(azure_connector.router, tags=['Azure'], prefix='/azc')



@app.get("/")
async def root():
    return {"message": "Welcome to Home Heal server!"}

# app.mount("/", socketio_app)
port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    kwargs = {"host": "localhost", "port": port}
    kwargs.update({"debug": True, "reload": True})
    uvicorn.run('main:app', reload=True)
