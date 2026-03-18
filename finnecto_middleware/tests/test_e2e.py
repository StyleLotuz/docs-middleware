from unittest.mock import patch, AsyncMock
from datetime import datetime, timedelta, UTC

import jwt
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

def _generate_token(connection_type: str, **extra_claims) -> str:
    payload = {
        "connection_type": connection_type,
        "username": "test_user",
        "password": "test_pass",
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC) + timedelta(hours=1),
        **extra_claims
    }
    return jwt.encode(payload, "incoming-jwt-dev-secret", algorithm="HS256")

SAMPLE_BODY = {
    "number": "FNCT0006",
    "reception_date": "2026-03-03",
    "due_date": "2026-03-20",
    "currency": "COP",
    "total": 780000,
    "items": [
        {
            "description": "Item 1",
            "unit_price": 30000,
            "total": 390000,
            "account": "VISTA"
        }
    ]
}

MOCK_LEGACY_RESPONSE = {
    "invoice_number": "FNCT0006",
    "recv_date": "2026-03-03",
    "expiry_date": "2026-03-20",
    "curr": "COP",
    "gross_total": 464100,
    "lines": [
        {
            "id": "ID-123",
            "desc": "Item 1",
            "unit_price": 30000,
            "line_total": 464100,
            "acct": "VISTA",
        }
    ],
    "processed_at": "2026-03-17T00:00:00Z"
}

MOCK_TAXEABLE_RESPONSE = {
    "document": {
        "reference": "FNCT0006",
        "dates": {
            "reception": "2026-03-03",
            "due": "2026-03-20",
        },
        "currency": "COP",
        "total": 390000,
        "items": [
            {
                "id": "ID-456",
                "description": "Item 1",
                "unitPrice": 30000,
                "amount": 390000,
                "account": "VISTA"
            }
        ],
        "processedAt": "2026-03-17T00:00:00Z",
    }
}

@pytest.mark.asyncio
@patch("modules.invoice.application.use_cases.invoice_forward_use_case.forward_request",new_callable=AsyncMock)
async def test_legacy_happy_path(mock_forward):
    mock_forward.return_value = MOCK_LEGACY_RESPONSE
    token = _generate_token("legacy")
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/invoice/forward",
            json=SAMPLE_BODY,
            headers={"Authorization": f"Bearer {token}"},
        )
        
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["message"] == "success invoice forward"
    assert data["item"]["number"] == "FNCT0006"
    assert data["errors"] is None
    
@pytest.mark.asyncio
@patch("modules.invoice.application.use_cases.invoice_forward_use_case.forward_request", new_callable=AsyncMock)
async def test_taxeable_happy_path(mock_forward):
    mock_forward.return_value = MOCK_TAXEABLE_RESPONSE
    token = _generate_token("taxeable", secret="mock-jwt-secret")
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/invoice/forward",
            json=SAMPLE_BODY,
            headers={"Authorization": f"Bearer {token}"},
        )
        
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["item"]["number"] == "FNCT0006"
    
@pytest.mark.asyncio
async def test_invalid_jwt_returns_401():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/invoice/forward",
            json=SAMPLE_BODY,
            headers={"Authorization": "Bearer invalid.token.here"},
        )
    
    assert response.status_code == 401
    data = response.json()
    assert data["status"] == 401
    
@pytest.mark.asyncio
async def test_missing_auth_returns_401():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/invoice/forward",
            json=SAMPLE_BODY
        )
        
    assert response.status_code == 401
    
@pytest.mark.asyncio
async def test_invalid_body_returns_400():
    token = _generate_token("legacy")
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/invoice/forward",
            json={"invalid": "body"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == 400
    assert data["errors"] is not None
    
@pytest.mark.asyncio
@patch("modules.invoice.application.use_cases.invoice_forward_use_case.forward_request", new_callable=AsyncMock)
async def test_mock_down_returns_502(mock_forward):
    import httpx
    mock_forward.side_effect = httpx.ConnectError("Connection refused")
    token = _generate_token("legacy")
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/invoice/forward",
            json=SAMPLE_BODY,
            headers={"Authorization": f"Bearer {token}"},
        )
    
    assert response.status_code == 502