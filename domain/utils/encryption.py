import hashlib


def sha256_hash(text: str) -> str:
    encoded_text = text.encode('utf-8')
    hash_object = hashlib.sha256(encoded_text)
    return hash_object.hexdigest()
