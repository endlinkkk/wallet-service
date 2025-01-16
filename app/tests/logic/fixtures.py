import pytest_asyncio
from domain.entities.wallets import Wallet as WalletEntity
from infra.database.models import Base
from infra.repositories.transactions.sqlalchemy_transaction_repository import SQLAlchemyTransactionRepository
from infra.repositories.wallets.sqlalchemy_wallet_repository import SQLAlchemyWalletRepository
from logic.services.transactions import TransactionService
from logic.services.wallets import WalletManagementService, WalletService
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class DatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    async def init_models(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="session")
async def database_manager():
    database_url = "sqlite+aiosqlite:///:memory:"
    manager = DatabaseManager(database_url)
    await manager.init_models()
    return manager


@pytest_asyncio.fixture(scope="session")
async def wallet_service(database_manager: DatabaseManager) -> WalletService:
    return WalletService(session_factory=database_manager.SessionLocal, wallet_repository=SQLAlchemyWalletRepository())


@pytest_asyncio.fixture(scope="session")
async def wallet_manager_service() -> WalletManagementService:
    return WalletManagementService(wallet_repository=SQLAlchemyWalletRepository())


@pytest_asyncio.fixture(scope="session")
async def transaction_service(
    database_manager: DatabaseManager, wallet_manager_service: WalletManagementService
) -> TransactionService:
    return TransactionService(
        session_factory=database_manager.SessionLocal,
        transaction_repository=SQLAlchemyTransactionRepository(),
        wallet_manager_service=wallet_manager_service,
    )


@pytest_asyncio.fixture(scope="session")
async def wallet(wallet_service: WalletService) -> WalletEntity:
    wallet = WalletEntity()
    return await wallet_service.create_wallet(wallet=wallet)
