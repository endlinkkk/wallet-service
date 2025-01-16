from contextlib import asynccontextmanager

from application.api.wallets.v1.handlers import router as wallet_router
from fastapi import FastAPI
from infra.database.manager import DatabaseManager
from logic.initial_container import init_container
from punq import Container


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()
    database_manager: DatabaseManager = container.resolve(DatabaseManager)
    await database_manager.init_models()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Wallet Service",
        docs_url="/api/docs",
        debug=True,
        lifespan=lifespan,
    )
    app.include_router(wallet_router, prefix="/v1/wallets")

    return app
