from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
from middlewares.error import ErrorHandler
from routers.sockets import socketio_app
from database.db import Base, engine
from routers import user, rol,account, menu, rol_menu

import uvicorn


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.title = "Home Heal API"
app.version = "1.0"

#Adicion de middlewares
app.add_middleware(ErrorHandler)
origins = ["http://localhost:4200"]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])


# Adición de routers
app.include_router(account.router, tags=["Accounts"], prefix="/account")
app.include_router(user.router, tags=["Users"], prefix="/user")
app.include_router(rol.router, tags=["Roles"], prefix="/rol")
app.include_router(menu.router, tags=["Menus"], prefix="/menu")
app.include_router(rol_menu.router, tags=["RolesMenus"], prefix="/rol_menu")


@app.get("/")
async def root():
    return {"message": "Welcome to Home Heal server!"}

app.mount("/", socketio_app)

if __name__ == "__main__":
    kwargs = {"host": "localhost", "port": 8000}
    kwargs.update({"debug": True, "reload": True})
    uvicorn.run('main:app', reload=True)
