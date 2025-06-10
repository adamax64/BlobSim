from data.db.db_engine import User, transactional
from data.persistence.user_repository import get_user_by_name
from .utils.encryption import sha256_hash


@transactional
def validate_credentials(username: str, password: str, session=None) -> bool:
    try:
        user: User = get_user_by_name(username, session)
        return user is not None and user.password == sha256_hash(password)
    except Exception as e:
        print(e)
        return False
