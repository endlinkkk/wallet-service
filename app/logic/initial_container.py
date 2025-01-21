from functools import lru_cache

from punq import (
    Container,
    Scope,
)

from infra.database.manager import (
    DatabaseManager,
    SessionManager,
)
from infra.repositories.transactions.base import BaseTransactionRepository
from infra.repositories.transactions.sqlalchemy_transaction_repository import SQLAlchemyTransactionRepository
from infra.repositories.wallets.base import BaseWalletRepository
from infra.repositories.wallets.sqlalchemy_wallet_repository import SQLAlchemyWalletRepository
from logic.services.transactions import (
    BaseTransactionService,
    TransactionService,
)
from logic.services.wallets import (
    BaseWalletManagementService,
    BaseWalletService,
    WalletManagementService,
    WalletService,
)
from logic.use_cases.transactions.create import CreateTransactionUseCase
from logic.use_cases.transactions.get import GetTransactionsUseCase
from logic.use_cases.wallets.create import CreateWalletUseCase
from logic.use_cases.wallets.get import GetWalletUseCase
from logic.validators.transactions import (
    BaseTransactionValidatorService,
    ComposedTaskValidatorService,
    TransactionAmountValidatorService,
    TransactionOperationTypeValidatorService,
)
from settings.config import Settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Settings, instance=Settings(), scope=Scope.singleton)
    settings: Settings = container.resolve(Settings)

    database_manager = DatabaseManager(settings.db_url)
    container.register(
        DatabaseManager,
        instance=database_manager,
        scope=Scope.singleton,
    )

    session_manager = SessionManager(session_factory=database_manager.SessionLocal)
    container.register(SessionManager, instance=session_manager)
    ### Wallets

    # wallet repository
    def build_wallet_repository() -> SQLAlchemyWalletRepository:
        return SQLAlchemyWalletRepository()

    container.register(BaseWalletRepository, factory=build_wallet_repository)

    # wallet services

    def init_wallet_managment_service() -> WalletManagementService:
        return WalletManagementService(
            wallet_repository=container.resolve(BaseWalletRepository),
        )

    def init_wallet_query_service() -> WalletService:
        return WalletService(
            session_manager=container.resolve(SessionManager),
            wallet_repository=container.resolve(BaseWalletRepository),
        )

    container.register(BaseWalletManagementService, factory=init_wallet_managment_service)
    container.register(BaseWalletService, factory=init_wallet_query_service)

    # wallet use cases
    def build_create_wallet_use_case() -> CreateWalletUseCase:
        return CreateWalletUseCase(
            wallet_service=container.resolve(BaseWalletService),
        )
    def build_get_wallet_use_case() -> GetWalletUseCase:
        return GetWalletUseCase(
            wallet_service=container.resolve(BaseWalletService),
        )
    container.register(CreateWalletUseCase, factory=build_create_wallet_use_case)
    container.register(GetWalletUseCase, factory=build_get_wallet_use_case)

    ### Transactions

    # validators
    container.register(TransactionAmountValidatorService)
    container.register(TransactionOperationTypeValidatorService)

    def build_transaction_validators() -> BaseTransactionValidatorService:
        return ComposedTaskValidatorService(
            validators=[
                container.resolve(TransactionAmountValidatorService),
                container.resolve(TransactionOperationTypeValidatorService),
            ],
        )

    container.register(BaseTransactionValidatorService, factory=build_transaction_validators)

    # transaction repository
    def build_transaction_repository() -> SQLAlchemyTransactionRepository:
        return SQLAlchemyTransactionRepository()

    container.register(BaseTransactionRepository, factory=build_transaction_repository)

    # transaction services

    def init_transaction_service() -> TransactionService:
        return TransactionService(
            session_manager=container.resolve(SessionManager),
            transaction_repository=container.resolve(BaseTransactionRepository),
            wallet_manager_service=container.resolve(BaseWalletManagementService),
        )

    container.register(BaseTransactionService, factory=init_transaction_service)

    # transactions use cases
    def build_create_transaction_use_case() -> CreateTransactionUseCase:
        return CreateTransactionUseCase(
            transaction_service=container.resolve(BaseTransactionService),
            validator_service=container.resolve(BaseTransactionValidatorService),
        )

    def build_get_transaction_use_case() -> GetTransactionsUseCase:
        return GetTransactionsUseCase(
            transaction_service=container.resolve(BaseTransactionService),
        )

    container.register(CreateTransactionUseCase, factory=build_create_transaction_use_case)
    container.register(GetTransactionsUseCase, factory=build_get_transaction_use_case)

    return container
