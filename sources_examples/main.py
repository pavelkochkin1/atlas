import os

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from utils import read_file_content

app = FastAPI(title="Mock Service for Agent via os.walk")

BASE_DIR = "./"
CONFLUENCE_DIR = os.path.join(BASE_DIR, "confluence")
GITLAB_DIR = os.path.join(BASE_DIR, "gitlab")
MTS_SCHEMA_PATH = os.path.join(BASE_DIR, "mts_schema.txt")


@app.get("/schema")
def get_schema():
    """
    Возвращает список таблиц из mts_schema.txt
    """
    if not os.path.exists(MTS_SCHEMA_PATH):
        raise HTTPException(status_code=404, detail="mts_schema.txt не найден")
    with open(MTS_SCHEMA_PATH, "r", encoding="utf-8") as f:
        tables = [line.strip() for line in f if line.strip()]
    return {"tables": tables}


@app.get("/confluence")
def search_confluence(table: str = Query(..., description="Название таблицы/витрины для поиска в Confluence")):
    """
    Ищет файлы внутри папки confluence (и её поддиректорий).
    Если table.lower() содержится в имени файла или в содержимом файла,
    то возвращаем содержимое этого файла.
    """
    if not os.path.exists(CONFLUENCE_DIR):
        raise HTTPException(status_code=500, detail="Папка Confluence не найдена")

    matched = []
    for root, _, files in os.walk(CONFLUENCE_DIR):
        for file in files:
            if file.lower().endswith(".md"):
                file_path = os.path.join(root, file)
                content = read_file_content(file_path)
                if table.lower() in file.lower() or table.lower() in content.lower():
                    matched.append({"file_name": file, "content": content})

    if not matched:
        raise HTTPException(status_code=404, detail="Совпадений в Confluence не найдено")
    return {"results": matched}


@app.get("/gitlab")
def search_gitlab(table: str = Query(..., description="Название таблицы/витрины для поиска в GitLab")):
    """
    Аналогичный поиск, но в папке gitlab (и её поддиректориях).
    Если table.lower() содержится в имени файла или в содержимом файла,
    то возвращаем текст кода Spark из этого файла.
    """
    if not os.path.exists(GITLAB_DIR):
        raise HTTPException(status_code=500, detail="Папка GitLab не найдена")

    matched = []
    for root, _, files in os.walk(GITLAB_DIR):
        for file in files:
            if file.lower().endswith(".py"):
                file_path = os.path.join(root, file)
                content = read_file_content(file_path)
                if table.lower() in file.lower() or table.lower() in content.lower():
                    matched.append({"file_name": file, "content": content})

    if not matched:
        raise HTTPException(status_code=404, detail="Совпадений в GitLab не найдено")
    return {"results": matched}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
