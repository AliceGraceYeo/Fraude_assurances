from fastapi import FastAPI
from routers import auth, admin, agent

app = FastAPI(title="Fraud Detection API", version="1.0")

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(agent.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Fraud Detection API"}