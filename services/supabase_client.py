from supabase import create_client
from core.config import settings

# Client public (pour les actions utilisateur)
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

# Client service (pour les actions admin côté serveur)
supabase_admin = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)