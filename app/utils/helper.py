import os
import hashlib
from pathlib import Path


def create_directory(path: str) -> None:
    """
    Create a directory if it does not exist.
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def get_file_extension(filename: str) -> str:
    """
    Return the file extension.
    """
    return os.path.splitext(filename)[1].lower()


def calculate_file_hash(file_path: str) -> str:
    """
    Calculate SHA-256 hash of a file.
    """
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            sha256.update(chunk)

    return sha256.hexdigest()


def format_file_size(size: int) -> str:
    """
    Convert bytes into a readable format.
    """
    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:
        if value < 1024:
            return f"{value:.2f} {unit}"
        value /= 1024

    return f"{value:.2f} PB"


def allowed_document(filename: str) -> bool:
    """
    Check if the document type is supported.
    """
    allowed_extensions = {
        ".pdf",
        ".docx",
        ".doc",
        ".pptx",
        ".xlsx",
        ".txt"
    }

    extension = get_file_extension(filename)

    return extension in allowed_extensions