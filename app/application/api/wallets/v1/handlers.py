from application.api.filters import PaginationIn
from application.api.schemas import ErrorSchema
from application.api.wallets.v1.schemas import (
    GetTransactionsQueryResponseSchema,
    InTransactionSchema,
    InWalletSchema,
    OutTransactionSchema,
    OutWalletSchema,
)
from domain.exceptions import ApplicationException
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.routing import APIRouter
from logic.initial_container import init_container
from logic.use_cases.transactions.create import CreateTransactionUseCase
from logic.use_cases.transactions.get import GetTransactionsUseCase
from logic.use_cases.wallets.create import CreateWalletUseCase
from logic.use_cases.wallets.get import GetWalletUseCase
from punq import Container

router = APIRouter(
    tags=["Wallet V1"],
)


@router.post(
    "/{wallet_uuid}/operation",
    status_code=status.HTTP_201_CREATED,
    description="Create new transaction",
    responses={
        status.HTTP_201_CREATED: {"model": OutTransactionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_transaction_handler(
    wallet_uuid: str,
    schema: InTransactionSchema,
    container: Container = Depends(init_container),  # noqa: B008
) -> OutTransactionSchema:
    use_case: CreateTransactionUseCase = container.resolve(CreateTransactionUseCase)

    try:
        transaction = await use_case.execute(transaction=schema.to_entity(wallet_oid=wallet_uuid))
    except ApplicationException as exception:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return OutTransactionSchema.from_entity(transaction=transaction)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Create new wallet",
    responses={
        status.HTTP_201_CREATED: {"model": OutWalletSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_wallet_handler(
    schema: InWalletSchema,
    container: Container = Depends(init_container),  # noqa: B008
) -> OutWalletSchema:
    use_case: CreateWalletUseCase = container.resolve(CreateWalletUseCase)

    try:
        wallet = await use_case.execute(wallet=schema.to_entity())
    except ApplicationException as exception:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return OutWalletSchema.from_entity(wallet=wallet)


@router.get(
    "/{wallet_uuid}",
    status_code=status.HTTP_200_OK,
    description="Get wallet",
    responses={
        status.HTTP_200_OK: {"model": OutWalletSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_wallet_handler(wallet_uuid: str, container: Container = Depends(init_container)) -> OutWalletSchema:  # noqa: B008
    use_case: GetWalletUseCase = container.resolve(GetWalletUseCase)

    try:
        wallet = await use_case.execute(wallet_oid=wallet_uuid)
    except ApplicationException as exception:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return OutWalletSchema.from_entity(wallet=wallet)


@router.get(
    "/{wallet_uuid}/transactions",
    status_code=status.HTTP_200_OK,
    description="Get transactions by wallet uuid",
    responses={
        status.HTTP_200_OK: {"model": GetTransactionsQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_transactions_handler(
    wallet_uuid: str,
    pagination_in: PaginationIn = Depends(),  # noqa: B008
    container: Container = Depends(init_container),  # noqa: B008
) -> GetTransactionsQueryResponseSchema:
    use_case: GetTransactionsUseCase = container.resolve(GetTransactionsUseCase)

    try:
        transactions = await use_case.execute(wallet_oid=wallet_uuid, pagination=pagination_in)
    except ApplicationException as exception:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return GetTransactionsQueryResponseSchema(
        count=len(transactions),
        limit=pagination_in.limit,
        offset=pagination_in.offset,
        items=[OutTransactionSchema.from_entity(transaction) for transaction in transactions],
    )
