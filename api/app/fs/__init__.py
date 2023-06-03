from pathlib import Path

from app import config


def make_user_dir(user_id: int) -> Path:
    if not config.STORAGE_LOCAL_BASE_PATH.is_dir():
        raise Exception
    user_path = config.STORAGE_LOCAL_BASE_PATH / str(user_id)

    Path.mkdir(user_path)

    return user_path
