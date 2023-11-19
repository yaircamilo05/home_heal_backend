# from fastapi.encoders import jsonable_encoder
# import socketio

# socketio_server = socketio.AsyncServer(
#     async_mode="asgi",
#     cors_allowed_origins=[]
# )

# socketio_app = socketio.ASGIApp(
#     socketio_server=socketio_server,
#     socketio_path="sockets"
# )

# @socketio_server.event
# async def connection(sid,environment,auth):
#     print("Nuevo usuario Conectado: ", sid)
#     await socketio_server.emit("join", {"Message": "Conectado al servidor Socket", "sid": sid})



# @socketio_server.event
# async def sendmessage(sid, data):
#     #guaradar el historioa de mensajes 
#     #obtenr todos los mensajes del usuario
#     data["type"] = 2
#     await socketio_server.emit("recivedmessage", jsonable_encoder(data), skip_sid=sid)



# @socketio_server.event
# async def disconnect(sid):
#     print("Usuario desconectado: ", sid)
#     await socketio_server.emit("disconnect", {"sid":sid})

# @socketio_server.event
# async def error(sid):
#     print("Error al intentar contectar: ", sid)
#     await socketio_server.emit("error", {"sid":sid})

