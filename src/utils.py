from fastapi import UploadFile

from os import mkdir, remove
from os.path import exists
from shutil import copyfileobj

from uuid import uuid4

TEMP_DIR = "temp"

if not exists(TEMP_DIR):
    mkdir(TEMP_DIR)


def save_temp_file(path: UploadFile) -> str:
    """Save temp file.

    Args:
        path (UploadFile): temp file.

    Returns:
        str: file path.
    """
    id = str(uuid4())

    file_location = f"{TEMP_DIR}/{id}-{path.filename}"

    with open(file_location, "wb") as f:
        copyfileobj(path.file, f)

    return file_location


def remove_temp_file(path: str) -> None:
    """Remove temp file.

    Args:
        path (str): temp file path.
    """
    remove(path)
