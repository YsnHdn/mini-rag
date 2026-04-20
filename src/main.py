from fastapi import FastAPI
from routes import base , data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    settings = get_settings()
    
    # On attache directement à app
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongo_db = app.mongo_conn[settings.MONGODB_DATABASE]
    
    yield
    
    # --- Shutdown ---
    app.mongo_conn.close()

app.include_router(base.base_router)
app.include_router(data.data_router)