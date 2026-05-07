# agent.py
from fastapi import APIRouter, Depends
from core.security import require_agent

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.get("/mes-dossiers")
async def mes_dossiers(current=Depends(require_agent)):
    user_id = current["user"].id
    # Ici tu requêteras ta table de dossiers filtrée par agent
    return {"agent": current["profile"]["full_name"], "dossiers": []}