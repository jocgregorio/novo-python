from typing import Any, Dict, Optional
from app.nocodb.client import nocodb_client

TABLE_REGISTRO_INICIAL = "mucsj28ln1jblhn"
TABLE_CLIENTE = "m9k34vkkkxsjvjx"
TABLE_EDUCACION_FORMAL = "mdrpxkkjnek3bnz"
TABLE_EDUCACION_COMPLEMENTARIA = "m5ep5vrkxeh1cj2"
TABLE_EXPERIENCIA_LABORAL = "meep3gzbjy5npny"
TABLE_HABILIDADES = "m4556t35kl1yd8h"

async def buscar_registro_inicial(id_slack: str) -> Optional[dict]:
    params = {"where": f"(ID_Slack,eq,{id_slack})", "limit": 1}
    records = await nocodb_client.get_records(TABLE_REGISTRO_INICIAL, params)
    return records[0] if records else None

async def crear_cliente(payload: Dict[str, Any]) -> dict:
    return await nocodb_client.create_record(TABLE_CLIENTE, payload)

async def actualizar_cliente(payload: Dict[str, Any]) -> dict:
    return await nocodb_client.update_record(TABLE_CLIENTE, payload)

async def crear_educacion_formal(payload: Dict[str, Any]) -> dict:
    return await nocodb_client.create_record(TABLE_EDUCACION_FORMAL, payload)

async def crear_educacion_complementaria(payload: Dict[str, Any]) -> dict:
    return await nocodb_client.create_record(TABLE_EDUCACION_COMPLEMENTARIA, payload)

async def crear_experiencia_laboral(payload: Dict[str, Any]) -> dict:
    return await nocodb_client.create_record(TABLE_EXPERIENCIA_LABORAL, payload)

async def crear_habilidad(payload: Dict[str, Any]) -> dict:
    return await nocodb_client.create_record(TABLE_HABILIDADES, payload)
