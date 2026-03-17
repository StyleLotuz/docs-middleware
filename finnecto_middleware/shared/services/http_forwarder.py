import logging
from typing import Any
import httpx
from config import settings

logger = logging.getLogger(__name__)

ENDPOINT_MAP = {
    "legacy": "/legacy",
    "taxeable": "/taxeable"
}

TIMEOUT_SECOND = 10

async def forward_request(
    connection_type: str,
    body: dict[str, Any],
    auth_header: str
) -> dict[str, Any]:
    endpoint = ENDPOINT_MAP.get(connection_type)
    if not endpoint:
        raise ValueError(f"Unknown connection type: {connection_type}")
    url = f"{settings.mock_server_url}{endpoint}"
    async with httpx.AsyncClient(timeout=TIMEOUT_SECOND) as client:
        response = await client.post(
            url, 
            json=body,
            headers={"Authorization": auth_header}
        )
        
    logger.info("Response received | status=%s", response.status_code)
    response.raise_for_status()
    return response.json()