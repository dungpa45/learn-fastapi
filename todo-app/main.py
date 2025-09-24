from fastapi import FastAPI
from routers import user, company, task
from database import engine, Base

from passlib.context import CryptContext


app = FastAPI(
    title="To-do API",
    description="A simple FastAPI for managing to-do tasks with users and companies.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
Base.metadata.create_all(bind=engine)  # create tables

app.include_router(user.router)
app.include_router(company.router)
app.include_router(task.router)