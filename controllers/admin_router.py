from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import subprocess
import os
import shutil
from datetime import datetime
from .auth_dependency import require_auth
from domain.admin_service import get_enabled_cronjobs, set_enabled_cronjobs
from domain.scheduler_service import start_scheduler, stop_scheduler

router = APIRouter(prefix="/admin", tags=["admin"])


def find_pg_dump() -> str:
    """
    Find pg_dump executable in PATH, PG_DUMP_PATH environment variable, or common PostgreSQL installation locations.
    Raises HTTPException if pg_dump is not found.
    """
    # First, check if PG_DUMP_PATH environment variable is set
    pg_dump_path = os.environ.get("PG_DUMP_PATH")
    if pg_dump_path and os.path.exists(pg_dump_path):
        return pg_dump_path

    # Second, try to find pg_dump in PATH
    pg_dump_path = shutil.which("pg_dump")
    if pg_dump_path:
        return pg_dump_path

    raise HTTPException(
        status_code=500,
        detail="pg_dump not found. Please ensure PostgreSQL is installed and either pg_dump is in your system PATH or set the PG_DUMP_PATH environment variable to the full path of pg_dump.exe.",
    )


@router.get("/db-dump")
async def download_database_dump(_: str = Depends(require_auth)):
    """
    Download the entire database as a SQL dump.
    Requires admin authentication.
    """

    # Find pg_dump executable
    pg_dump_path = find_pg_dump()

    # Database connection details from environment
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "bcs_database")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")

    # Command to dump the database in plain SQL format
    cmd = [
        pg_dump_path,
        "-U",
        POSTGRES_USER,
        "-h",
        POSTGRES_HOST,
        "-p",
        POSTGRES_PORT,
        "-d",
        POSTGRES_DB,
        "--format=plain",  # Plain SQL text
        "--no-owner",  # Don't include ownership commands
        "--no-privileges",  # Don't include privilege commands
        "--clean",  # Include commands to clean (drop) database objects
        "--if-exists",  # Use IF EXISTS when dropping objects
    ]

    # Set environment for password
    env = os.environ.copy()
    env["PGPASSWORD"] = POSTGRES_PASSWORD

    try:
        # Run pg_dump
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            timeout=300,  # 5 minute timeout
        )

        if result.returncode != 0:
            raise HTTPException(
                status_code=500, detail=f"Database dump failed: {result.stderr}"
            )

        # Return the SQL dump as a downloadable file
        def iter_sql():
            yield result.stdout

        # Generate filename with current date in YYYYMMDD format
        now = datetime.now()
        date_str = now.strftime("%Y%m%d")
        filename = f"bcs_dump_{date_str}.sql"

        return StreamingResponse(
            iter_sql(),
            media_type="application/sql",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Database dump timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/cronjobs-enabled")
async def get_cronjobs_enabled(_: str = Depends(require_auth)):
    """
    Get the current state of enabled cronjobs.
    Requires admin authentication.
    """
    try:
        enabled = get_enabled_cronjobs()
        return {"enabled": enabled}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get cronjobs status: {str(e)}"
        )


@router.post("/cronjobs-enabled")
async def set_cronjobs_enabled(enabled: bool, _: str = Depends(require_auth)):
    """
    Set the enabled state of cronjobs.
    Requires admin authentication.
    """
    try:
        set_enabled_cronjobs(enabled=enabled)

        # Dynamically start/stop the scheduler
        if enabled:
            start_scheduler()
        else:
            stop_scheduler()

        return {
            "enabled": enabled,
            "message": f"Cronjobs {'enabled' if enabled else 'disabled'} successfully",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to set cronjobs status: {str(e)}"
        )
