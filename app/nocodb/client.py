import httpx
from typing import Any, Dict, Optional
from app.core.config import settings

class NocoDBClient:
    def __init__(self):
        self.base_url = settings.NOCODB_BASE_URL.rstrip('/')
        self.headers = {
            "xc-token": settings.NOCODB_API_TOKEN,
            "Content-Type": "application/json"
        }

    async def get_records(self, table_id: str, params: Optional[Dict[str, Any]] = None) -> list[dict]:
        url = f"{self.base_url}/api/v2/tables/{table_id}/records"
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("list", [])

    async def create_record(self, table_id: str, payload: Dict[str, Any]) -> dict:
        url = f"{self.base_url}/api/v2/tables/{table_id}/records"
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def update_record(self, table_id: str, payload: Dict[str, Any]) -> dict:
        url = f"{self.base_url}/api/v2/tables/{table_id}/records"
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.patch(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()

nocodb_client = NocoDBClient()
