from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from config.database import engine, Base
from middelwares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

import os
import uvicorn

#pip install fastapi   --> Instalación de FastAPI
#pip install uvicorn   --> Instalación de Uvicorn para ejecutar el servidor
# uvicorn main:app --reload --port 8001 --host 0.0.0.0   --> Ejecución del servidor
#http://localhost:8001/docs#/   --> Documentación de la API


app = FastAPI()
app.title = "My first API"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


# Rutas de la API 

@app.get('/', tags=['home'])
def message():
    return HTMLResponse(content="<h1>My first API</h1>", status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(os.environ.get("PORT", 8000)))


