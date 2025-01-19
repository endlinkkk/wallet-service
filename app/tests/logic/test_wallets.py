import pytest

from application.api.filters import PaginationIn
from domain.entities.wallets import (
    OperationType,
    Transaction as TransactionEntity,
    Wallet as WalletEntity,
)
from logic.exceptions.wallets import (
    NotEnoughFundsException,
    WalletNotFoundException,
)
from logic.services.transactions import TransactionService


@pytest.mark.asyncio
async def test_add_transaction(transaction_service: TransactionService, wallet: WalletEntity):
    transaction = TransactionEntity(
        operation_type="DEPOSIT",
        amount=100,
        wallet_oid=wallet.oid,
    )
    saved_transaction = await transaction_service.create_transaction(transaction)
    assert saved_transaction.oid == transaction.oid
    assert saved_transaction.wallet_oid == wallet.oid


@pytest.mark.asyncio
async def test_get_transaction_list(transaction_service: TransactionService, wallet: WalletEntity):
    pagination = PaginationIn(limit=10, offset=0)
    transactions = await transaction_service.get_transactions_list(wallet_oid=wallet.oid, pagination=pagination)
    assert isinstance(transactions, list)
    assert len(transactions) == 1


@pytest.mark.asyncio
async def test_wallet_not_found_exception(transaction_service: TransactionService):
    transaction = TransactionEntity(
        operation_type="DEPOSIT",
        amount=100,
        wallet_oid="1234",
    )
    with pytest.raises(WalletNotFoundException):
        await transaction_service.create_transaction(transaction)


@pytest.mark.asyncio
async def test_not_enough_funds_exception(transaction_service: TransactionService, wallet: WalletEntity):
    transaction = TransactionEntity(
        operation_type=OperationType.WITHDRAW,
        amount=1000000,
        wallet_oid=wallet.oid,
    )
    with pytest.raises(NotEnoughFundsException):
        await transaction_service.create_transaction(transaction)
