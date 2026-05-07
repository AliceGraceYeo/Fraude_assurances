from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.supabase_client import supabase

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    """Vérifie le JWT Supabase et retourne l'utilisateur connecté."""
    token = credentials.credentials
    try:
        # Supabase valide le JWT et retourne l'utilisateur
        response = supabase.auth.get_user(token)
        user = response.user
        if not user:
            raise HTTPException(status_code=401, detail="Token invalide")
        
        # Récupère le profil pour avoir le rôle
        profile = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
        return {"user": user, "profile": profile.data, "token": token}
    except Exception:
        raise HTTPException(status_code=401, detail="Non authentifié")

async def require_admin(current=Depends(get_current_user)):
    """Autorise uniquement le rôle admin."""
    if current["profile"]["role"] != "admin":
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs")
    return current

async def require_agent(current=Depends(get_current_user)):
    """Autorise admin ET agent_assurance."""
    if current["profile"]["role"] not in ("admin", "agent_assurance"):
        raise HTTPException(status_code=403, detail="Accès refusé")
    return current