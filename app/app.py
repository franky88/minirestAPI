from fastapi import FastAPI
from server.routes import users, items, auth

app = FastAPI(
    version="0.1.0"
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth.router)

@app.get("/")
async def read_root():
    hash = users.pwd_context.hash("sample")
    is_valid = users.pwd_context.verify("sample", hash)
    return {
        "message": "API is ready!",
        "hash": hash,
        "is_valid": is_valid
    }