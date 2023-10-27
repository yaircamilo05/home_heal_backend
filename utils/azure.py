from fastapi import UploadFile
from fastapi import FastAPI, UploadFile, File
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

# Configura la conexión a Azure Blob Storage
connection_string = "DefaultEndpointsProtocol=https;AccountName=estremorstorageaccount;AccountKey=/mCPhntPNfJg04502cvRTNd1ZooObPUYWl9hC3fWv60h8bl/NHCfC8yTkGQkH7Z6PMIcmFgdrnQd+AStIQSUMA==;EndpointSuffix=core.windows.net"
container_name = "estremoruserscontainer"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)


def upload_file_to_azurecontainer(file: UploadFile, filename: str):
    if file is None:
        return None
    try:
        # Guarda el archivo en Azure Blob Storage
        blob_client = container_client.get_blob_client(filename)

        with file.file as f:
            blob_client.upload_blob(f, overwrite=True)
          # Devuelve la URL de la imagen
        image_url = f"https://{blob_client.account_name}.blob.core.windows.net/{container_name}/{filename}"
        return image_url
    except Exception as e:
        return {"error": str(e)}
    

    