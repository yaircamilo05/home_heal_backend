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
app.include_router(account.router, tags=["Account"])
app.include_router(user.router, tags=["User"])
app.include_router(rol.router, tags=["Rol"])
app.include_router(menu.router, tags=["Menu"])
app.include_router(rol_menu.router, tags=["RolMenu"])


@app.get("/")
async def root():
    return {"message": "Welcome to Home Heal server!"}

app.mount("/", socketio_app)

if __name__ == "__main__":
    kwargs = {"host": "0.0.0.0", "port": 8000}
    kwargs.update({"debug": True, "reload": True})
    uvicorn.run('main:app', reload=True)
