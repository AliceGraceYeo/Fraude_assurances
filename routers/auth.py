from fastapi import APIRouter, HTTPException
from models.user import LoginRequest, RegisterRequest
from services.supabase_client import supabase, supabase_admin

router = APIRouter(prefix="/auth", tags=["Authentification"])

@router.post("/login")
async def login(body: LoginRequest):
    """Connexion et retour du JWT."""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": body.email,
            "password": body.password
        })
        session = response.session
        user_id = response.user.id
        
        # Récupère le rôle depuis la table profiles
        profile = supabase.table("profiles").select("role, full_name").eq("id", user_id).single().execute()
        
        return {
            "access_token": session.access_token,
            "token_type": "bearer",
            "role": profile.data["role"],
            "full_name": profile.data["full_name"]
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

@router.post("/register")
async def register(body: RegisterRequest):
    """Création d'un compte (admin uniquement via service role)."""
    try:
        # Crée l'utilisateur dans Supabase Auth
        auth_response = supabase_admin.auth.admin.create_user({
            "email": body.email,
            "password": body.password,
            "email_confirm": True  # Confirme directement sans email
        })
        user_id = auth_response.user.id
        
        # Insère le profil avec le rôle
        supabase_admin.table("profiles").insert({
            "id": user_id,
            "email": body.email,
            "role": body.role,
            "full_name": body.full_name
        }).execute()
        
        return {"message": "Compte créé avec succès", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/logout")
async def logout():
    supabase.auth.sign_out()
    return {"message": "Déconnecté"}