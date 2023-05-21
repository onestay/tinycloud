from fastapi import FastAPI

from .routers import auth, files, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(files.router)


@app.get("/")
async def root():
    return {"message": "hello world!"}
