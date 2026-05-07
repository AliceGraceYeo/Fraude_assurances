# admin.py
from fastapi import APIRouter, Depends
from core.security import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
async def admin_dashboard(current=Depends(require_admin)):
    return {"message": f"Bienvenue admin {current['profile']['full_name']}"}

@router.get("/agents")  # Liste tous les agents
async def list_agents(current=Depends(require_admin)):
    from services.supabase_client import supabase_admin
    result = supabase_admin.table("profiles").select("*").eq("role", "agent_assurance").execute()
    return result.data