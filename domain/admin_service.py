from typing import Generator
from data.persistence.admin_repository import generate_database_dump, get_database_dump_filename


def create_database_dump() -> tuple[Generator[bytes, None, None], str]:
    """
    Creates a database dump and returns both the data stream and filename.

    Returns:
        tuple: (data_generator, filename) for the database dump
    """
    data_stream = generate_database_dump()
    filename = get_database_dump_filename()

    return data_stream, filename
