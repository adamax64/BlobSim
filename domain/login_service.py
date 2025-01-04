from data.persistence.user_repository import get_user_by_name, is_exist_by_name
from .utils.encryption import sha256_hash


def check_if_user_exists(username: str) -> bool:
    return is_exist_by_name(username)


def validate_credentials(username: str, password: str) -> bool:
    user = get_user_by_name(username)
    return user.password == sha256_hash(password)
