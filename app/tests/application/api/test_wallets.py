from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

import pytest
from httpx import Response


@pytest.fixture(scope="session")
def wallet(app: FastAPI, client: TestClient) -> dict:
    url = app.url_path_for("create_wallet_handler")
    response: Response = client.post(url=url, json={})
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


class TestWalletAndTransaction:
    def test_create_wallet_success(self, wallet):
        assert "uuid" in wallet

    def test_create_transaction_success(self, app: FastAPI, client: TestClient, wallet: dict):
        url = app.url_path_for("create_transaction_handler", wallet_uuid=wallet["uuid"])
        response: Response = client.post(url=url, json={"operationType": "DEPOSIT", "amount": 100})
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_transaction_failure_insufficient_funds(self, app: FastAPI, client: TestClient, wallet: dict):
        url = app.url_path_for("create_transaction_handler", wallet_uuid=wallet["uuid"])
        response: Response = client.post(url=url, json={"operationType": "WITHDRAW", "amount": 1000})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_wallet_transactions(self, app: FastAPI, client: TestClient, wallet: dict):
        url = app.url_path_for("get_transactions_handler", wallet_uuid=wallet["uuid"])
        response: Response = client.get(url=url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data.get("items"), list)
        assert len(data["items"]) == 1
