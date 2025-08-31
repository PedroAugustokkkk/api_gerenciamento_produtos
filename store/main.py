from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from store.core.config import settings
from store.routers import api_router
from store.core.exceptions import NotFoundException

# Cria a instância principal do FastAPI com configurações do projeto
app = FastAPI(
    version="0.0.1",
    title=settings.PROJECT_NAME,
    root_path=settings.ROOT_PATH
)

# Inclui as rotas da API definidas em api_router
app.include_router(api_router)

# Adiciona um manipulador de exceções para NotFoundException
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    # Retorna uma resposta JSON com status 404 e a mensagem da exceção
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )
