from fastapi import FastAPI
from app.database.db import engine, Base
from app.routers import auth, admin
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging


#Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Application
app = FastAPI(title = 'INAI API')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:5173'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)


# Files
app.mount('/media', StaticFiles(directory = 'app/media'), name = 'media')


# Tables
Base.metadata.create_all(bind = engine)


# Routers
app.include_router(auth.router)
app.include_router(admin.router)


@app.get('/')
def root(): return {'message': 'Backend part'}


if __name__ == '__main__':
    uvicorn.run(app = 'main:app', port = 8000, reload = True)