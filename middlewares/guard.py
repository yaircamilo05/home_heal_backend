from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from utils.jwt import validate_token


class NeedToken(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        if auth is None:
            raise HTTPException(
                status_code=401, detail="Not authorized add the token")
        return auth.credentials


class SuperAdmin(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['rol_id'] != 1:
            raise HTTPException(status_code=401, detail="Not authorized")


class Paciente(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['rol_id'] != 2:
            raise HTTPException(status_code=401, detail="Not authorized")


class Familiar(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['rol_id'] != 3:
            raise HTTPException(status_code=401, detail="Not authorized")


class Medico(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['rol_id'] != 4:
            raise HTTPException(status_code=401, detail="Not authorized")

class MedicoPaciente(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['rol_id'] != 4 and data['rol_id'] != 2:
            raise HTTPException(status_code=401, detail="Not authorized")
        
class MedicoFamiliar(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['rol_id'] != 4 and data['rol_id'] != 3:
            raise HTTPException(status_code=401, detail="Not authorized")
        
class FamiliarPaciente(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['rol_id'] != 3 and data['rol_id'] != 2:
            raise HTTPException(status_code=401, detail="Not authorized")
        