from fastapi import APIRouter
from schemas.key_schema import
APIKeyResponse
import secrets

router = APIRouter(prefix="/auth",
tags=["Authentication"])

@router.get("/get-key",
response_model=APIKeyResponse)
async def get_api_key(user_id: int):
    random_key = secrets.token_hex(16)
    return{
        "user_id": user_id,
        "api_key": f"redbus_{random_key}",
        "status": "active"
    }