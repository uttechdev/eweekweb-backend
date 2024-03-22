
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import router

load_dotenv()
# print(os.getenv("MONGO_URI"))
app = FastAPI(
    title="E-Week API",
    summary="A simple API to manage E-Week records.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify domains as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
