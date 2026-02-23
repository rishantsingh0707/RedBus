from fastapi import FastAPI
from routes.user_routes import router
from error_handlers import register_exception_handlers

app = FastAPI(title="RedBus Production API")

register_exception_handlers(app)
app.include_router(router)

@app.get("/")
def root():
    return {"message": "RedBus Backend Running"}

