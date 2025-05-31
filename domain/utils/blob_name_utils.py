def format_blob_name(blob) -> str:
    first = blob.first_name.strip() if blob.first_name else ""
    last = blob.last_name.strip() if blob.last_name else ""
    return f"{first} {last}".strip()
