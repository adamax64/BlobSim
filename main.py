from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from controllers import (
    action_router,
    auth_router,
    blobs_router,
    calendar_router,
    competition_router,
    event_record_router,
    factory_router,
    hall_of_fame_router,
    leagues_router,
    news_router,
    policies_router,
    sim_data_router,
    standings_router,
)
from domain.startup_service import startup

app = FastAPI()
app.title = "Blob Championship System API"

origins = [
    "http://localhost",
    "http://localhost:8000",  # BE URL
    "http://localhost:3000",  # DEV URL
    "http://localhost:3001",  # DEV URL
]

# Read production URLs from environment variables
progon_url_prod = os.environ.get("ORIGIN_URL")
if progon_url_prod:
    origins.append(progon_url_prod)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

startup()

app.include_router(sim_data_router.router)
app.include_router(blobs_router.router)
app.include_router(factory_router.router)
app.include_router(leagues_router.router)
app.include_router(standings_router.router)
app.include_router(competition_router.router)
app.include_router(action_router.router)
app.include_router(event_record_router.router)
app.include_router(hall_of_fame_router.router)
app.include_router(calendar_router.router)
app.include_router(auth_router.router)
app.include_router(news_router.router)
app.include_router(policies_router.router)
