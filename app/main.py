from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, external_data
from app.database import engine
from app.models import user

app = FastAPI()

user.base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(external_data.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "API para o projeto de Cloud 2024.2"}
