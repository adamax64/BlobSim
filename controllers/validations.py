from fastapi import HTTPException


def validate_blob_name(name: str):
    name = name.strip()
    words = name.split(' ')
    if not len(words) == 2:
        raise HTTPException(status_code=400, detail="Name should consist of two words")
    for word in words:
        if not word.istitle():
            raise HTTPException(status_code=400, detail="Each word should start with a capital letter")
