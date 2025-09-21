import subprocess
import os
from typing import Generator
from datetime import datetime
from data.db import db_engine


def generate_database_dump() -> Generator[bytes, None, None]:
    """
    Generates a PostgreSQL database dump using pg_dump.
    Returns a generator that yields chunks of the dump data.
    """
    POSTGRES_USER = db_engine.POSTGRES_USER
    POSTGRES_PASSWORD = db_engine.POSTGRES_PASSWORD
    POSTGRES_DB = db_engine.POSTGRES_DB
    POSTGRES_HOST = db_engine.POSTGRES_HOST
    POSTGRES_PORT = db_engine.POSTGRES_PORT

    # Set the password in the environment for pg_dump
    env = os.environ.copy()
    env["PGPASSWORD"] = POSTGRES_PASSWORD

    dump_cmd = [
        "pg_dump",
        "-h", POSTGRES_HOST,
        "-p", str(POSTGRES_PORT),
        "-U", POSTGRES_USER,
        "-d", POSTGRES_DB,
        "-F", "c"  # custom format, suitable for pgAdmin import
    ]

    process = subprocess.Popen(
        dump_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        bufsize=0  # Unbuffered output
    )

    try:
        # Read from stdout in chunks
        while True:
            chunk = process.stdout.read(8192)
            if not chunk:
                break
            yield chunk

        # Wait for process to complete and check for errors
        process.wait()
        if process.returncode != 0:
            stderr_output = process.stderr.read().decode('utf-8')
            raise Exception(f"pg_dump failed with return code {process.returncode}: {stderr_output}")
    except Exception as e:
        # Ensure process is terminated on error
        if process.poll() is None:
            process.terminate()
            process.wait()
        raise e
    finally:
        # Clean up file descriptors
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()


def get_database_dump_filename() -> str:
    """
    Returns the filename for the database dump file with current date.
    """
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{db_engine.POSTGRES_DB}_dump_{current_date}.pgadmin"
