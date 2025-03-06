from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import sim_data_router, general_info_router
from domain.startup_service import startup

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",  # BE URL
    "http://localhost:3000",  # DEV URL
    "http://localhost:3001",  # DEV URL
    "http://localhost:5173",  # PRD URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

startup()

app.include_router(sim_data_router.router)
app.include_router(general_info_router.router)
