from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine

from routers.sockets import socketio_app
from routers import rol

import uvicorn


Base.metadata.create_all(bind=engine)
app = FastAPI()

# Adición de routers
app.include_router(rol.rol_router, tags=["Rol"], prefix="/rol")

# Configura las políticas CORS
origins = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Home Heal server!"}

app.mount("/", socketio_app)

if __name__ == "__main__":
    kwargs = {"host":"0.0.0.0", "port":8000}
    kwargs.update({"debug":True, "reload":True})
    uvicorn.run('main:app',reload=True)