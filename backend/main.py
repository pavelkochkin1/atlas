from db.init_db import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import drafts_router, entities_router, relationships_router

app = FastAPI(title="Atlas Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Событие запуска FastAPI. Здесь можно вызывать функции,
    которые должны выполняться перед стартом приложения.
    """
    print("Запуск приложения... Инициализация Neo4j.")
    await init_db()


# Подключаем все наши роутеры
app.include_router(entities_router, prefix="/api", tags=["Entities"])
app.include_router(relationships_router, prefix="/api/relationships", tags=["Relationships"])
app.include_router(drafts_router, prefix="/api/drafts", tags=["Drafts"])
