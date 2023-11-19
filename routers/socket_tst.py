# from fastapi import APIRouter, HTTPException
# # from models import TelemedicineData  # Asumiendo que tienes un modelo definido
# import httpx  # Biblioteca para hacer solicitudes HTTP

# router = APIRouter()

# # Configuración de Azure Web PubSub
# webpubsub_endpoint = "https://home-heal-socket.webpubsub.azure.com"
# access_key = "NEJslgDLuf1j9i13Yq+K4sYev+CODLFWEs9aEQSyUzE="
# hub_name = "Hub"  # Nombre del hub que usarás en Azure Web PubSub

# @router.post("/telemedicine")
# async def receive_telemedicine_data(data: dict):
#     try:
#         # Convertir los datos a un formato adecuado (por ejemplo, JSON)
#         # json_data = data.json()

#         # Enviar los datos al canal de Azure Web PubSub
#         async with httpx.AsyncClient() as client:
#             response = await client.post(
#                 f"{webpubsub_endpoint}/api/hubs/{hub_name}",
#                 headers={"Authorization": f"Bearer {access_key}"},
#                 json={"type": "message", "data": data}
#             )
#         if response.status_code != 200:
#             raise HTTPException(status_code=response.status_code, detail="Error al enviar datos a Web PubSub")

#         return {"message": "Datos de telemedicina enviados correctamente."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))