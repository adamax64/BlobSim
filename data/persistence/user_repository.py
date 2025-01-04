from data.db.db_engine import User, transactional


@transactional
def is_exist_by_name(username: str, session=None) -> bool:
    query_result = session.query(User).filter(User.name == username).all()
    return not len(query_result) == 0


@transactional
def get_user_by_name(username: str, session=None) -> User:
    query_result = session.query(User).filter(User.name == username).all()

    if len(query_result) == 1:
        return query_result[0]
    elif len(query_result) == 0:
        raise Exception(f'No user found with name {username}')
    else:
        raise Exception(f'More than one user found with name {username}')
