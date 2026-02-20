from fastapi import FastAPI
from app.routes import user_routes
from routes import auth_key

app = FastAPI(title="RedBus Production API")
app.include_router(auth_key.router)

app.include_router(user_routes.router)

@app.get("/")
def root():
    return {"message": "RedBus Backend Running"}
