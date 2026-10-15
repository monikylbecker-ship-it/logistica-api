
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import motoristas, entregas


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas que ainda não existem.
    # Adequado para desenvolvimento inicial.
    Base.metadata.create_all(bind=engine)

    yield

    # Não é necessário fechar o engine a cada requisição.


app = FastAPI(
    title="Logística API",
    description=(
        "API RESTful para gestão de motoristas, "
        "fretes e entregas."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Registra os endpoints.
app.include_router(motoristas.router)
app.include_router(entregas.router)


@app.get("/", tags=["Inicial"])
def home():
    return {
        "mensagem": "API de Logística funcionando!",
        "documentacao": "/docs",
        "versao": "1.0.0",
    }


@app.get("/health", tags=["Inicial"])
def health():
    return {"status": "ok"}
