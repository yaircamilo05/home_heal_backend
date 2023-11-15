from fastapi import UploadFile
from fastapi import UploadFile
from azure.storage.blob import BlobServiceClient


# Configura la conexión a Azure Blob Storage
connection_string = 'DefaultEndpointsProtocol=https;AccountName=imgblobstorage;AccountKey=yK62qR/KVNHLgIM+1BL5NZ+1oAHVQMDvmr/SoCL2DjPgoBU0CT/qfXFvAYAaIp45t6QsPy8ae+wS+AStwVsgdQ==;EndpointSuffix=core.windows.net'

container_name = 'hh-user-images'


blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)
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
        image_url = f'https://{blob_client.account_name}.blob.core.windows.net/{
            container_name}/{filename}'
        return image_url
    except Exception as e:
        return {'error': str(e)}
