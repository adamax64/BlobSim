from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
import os
from contextlib import asynccontextmanager

from controllers import (
    action_router,
    admin_router,
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
from domain.admin_service import get_enabled_cronjobs
from domain.scheduler_service import (
    start_scheduler,
    stop_scheduler,
    is_scheduler_running,
)


# Read cronjobs setting from environment variable (recommended for fastapi dev)
ENABLE_CRONJOBS = os.getenv("ENABLE_CRONJOBS", "false").lower() == "true"


def get_cronjobs_enabled_setting() -> bool:
    """
    Get the cronjobs enabled setting from the database.
    Falls back to environment variable if database is not available.
    """
    try:
        return get_enabled_cronjobs()
    except Exception as e:
        print(f"[WARNING] Failed to read cronjobs setting from database: {e}")
        print("[INFO] Falling back to environment variable ENABLE_CRONJOBS")
        return ENABLE_CRONJOBS


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Get cronjobs setting from database
    cronjobs_enabled = get_cronjobs_enabled_setting()

    # Startup: start the scheduler if enabled
    if cronjobs_enabled:
        start_scheduler()
    else:
        print("[INFO] Cronjobs are disabled.")
    yield
    # Shutdown: stop the scheduler
    if is_scheduler_running():
        stop_scheduler()


app = FastAPI(lifespan=lifespan)
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

# If the app is behind a TLS-terminating reverse proxy (nginx), trust proxy headers
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
# Note: HTTPS redirect is handled by nginx (HTTP -> HTTPS redirect on port 80)
# HTTPSRedirectMiddleware is not needed when behind a reverse proxy and would cause issues
# since all requests from nginx appear as HTTP to the FastAPI app


@app.middleware("http")
async def hsts_middleware(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = (
        "max-age=63072000; includeSubDomains; preload"
    )
    return response


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
app.include_router(admin_router.router)
app.include_router(news_router.router)
app.include_router(policies_router.router)
