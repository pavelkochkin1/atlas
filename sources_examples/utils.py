import os

from fastapi import HTTPException


def read_file_content(full_path: str) -> str:
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения файла {os.path.basename(full_path)}: {e}")
