from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from utils.azure import upload_file_to_azurecontainer


router = APIRouter()
@router.post("/upload/")
async def upload_image(file: UploadFile):
    result = upload_file_to_azurecontainer(file=file, filename=file.filename)
    if result is None:
        return JSONResponse(status_code= 400, content={"error": "No se ha enviado ningún archivo"})
    return JSONResponse(status_code= 200, content=result)