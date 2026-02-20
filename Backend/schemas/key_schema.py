from pydantic import BaseModel

class APIKeyResponse(BaseModel):
    user_id: int
    api_key: str
    status: str = "active"