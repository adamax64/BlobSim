from fastapi import FastAPI

from controllers import sim_data_router
from domain.startup_service import startup

app = FastAPI()

startup()

app.include_router(sim_data_router.router)
