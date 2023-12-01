# from fastapi import APIRouter
# from services.azure_connector import AzureConnector
# from fastapi import WebSocket, WebSocketDisconnect

# router = APIRouter()
# # connector = AzureConnector()
# connected_clients = set()


# @router.get('/socket.io/{userId}')
# async def get_connection_token(userId: str):
#     # Genera un token de conexión para el cliente
#     token = connector.get_client_access_token()
#     return {'url': token['url']}


# @router.websocket('/ws/{client_id}')
# async def websocket_endpoint(websocket: WebSocket, client_id: str):
#     await websocket.accept()
#     connected_clients.add(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             message = f'Client {client_id}: {data}'
#             print(f'Received message: {message}')
#             # Aquí, en lugar de enviar a Azure, retransmite a todos los clientes conectados
#             print('Clientes Conectados: ', connected_clients)
#             for client in connected_clients:
#                 await client.send({"data": message})
#     except WebSocketDisconnect:
#         #connected_clients.remove(websocket)
#         print( f'Client {client_id} disconnected - Total Clients: {len(connected_clients)}')


# def send_message(self, message):
#     print(f'Sending message to Azure: {message}')  # Agregado para depuración
#     self._client.send_to_all(message)


