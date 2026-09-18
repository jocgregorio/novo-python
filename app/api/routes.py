from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel

from app.workflows.orchestrator import procesar_candidato


router = APIRouter()


class WebhookPayload(BaseModel):
    ID_Slack: str | None = None
    thread_ts: str | None = None


@router.post("/webhook/candidato", status_code=status.HTTP_202_ACCEPTED)
async def recibir_candidato(payload: WebhookPayload, background_tasks: BackgroundTasks):
    slack_id = payload.ID_Slack or payload.thread_ts

    if not slack_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se requiere ID_Slack o thread_ts.",
        )

    background_tasks.add_task(procesar_candidato, slack_id)
    return {
        "status": "processing",
        "message": "Procesamiento en segundo plano",
        "id_slack": slack_id,
    }


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
