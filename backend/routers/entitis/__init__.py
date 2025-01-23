from fastapi import APIRouter
from routers.entitis.field import fields_router
from routers.entitis.industry import industry_router
from routers.entitis.persons import person_router
from routers.entitis.semantic_block import sem_block_router
from routers.entitis.table import table_router
from routers.entitis.team import team_router

entities_router = APIRouter(prefix="/entities")
entities_router.include_router(fields_router)
entities_router.include_router(industry_router)
entities_router.include_router(person_router)
entities_router.include_router(table_router)
entities_router.include_router(team_router)
entities_router.include_router(sem_block_router)
