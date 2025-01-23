from typing import List

from db.neo4j_client import Neo4jClient, get_neo4j_client
from fastapi import APIRouter, Depends, HTTPException
from schemas.industry import Industry

industry_router = APIRouter(prefix="/industries")


@industry_router.post("/", response_model=Industry)
async def create_industry(industry_in: Industry, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    CREATE (i:Industry {id: $id, name: $name})
    RETURN i.id as id, i.name as name
    """
    result = await neo4j_client.run_query_single(query, {"id": industry_in.id, "name": industry_in.name})
    if not result:
        raise HTTPException(status_code=400, detail="Ошибка создания Industry")
    return Industry(id=result.get("id"), name=result.get("name"))


@industry_router.get("/", response_model=List[Industry])
async def get_industries(neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = "MATCH (i:Industry) RETURN i.id AS id, i.name AS name"
    results = await neo4j_client.run_query_all(query)
    return [Industry(id=r["id"], name=r["name"]) for r in results]


@industry_router.get("/{industry_id}", response_model=Industry)
async def get_industry(industry_id: str, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (i:Industry {id: $id})
    RETURN i.id AS id, i.name AS name
    """
    result = await neo4j_client.run_query_single(query, {"id": industry_id})
    if not result:
        raise HTTPException(status_code=404, detail="Industry не найдена")
    return Industry(id=result.get("id"), name=result.get("name"))


@industry_router.put("/{industry_id}", response_model=Industry)
async def update_industry(
    industry_id: str, industry_in: Industry, neo4j_client: Neo4jClient = Depends(get_neo4j_client)
):
    query = """
    MATCH (i:Industry {id: $id})
    SET i.name = $name
    RETURN i.id AS id, i.name AS name
    """
    result = await neo4j_client.run_query_single(query, {"id": industry_id, "name": industry_in.name})
    if not result:
        raise HTTPException(status_code=404, detail="Industry не найдена или ошибка при обновлении")
    return Industry(id=result.get("id"), name=result.get("name"))


@industry_router.delete("/{industry_id}")
async def delete_industry(industry_id: str, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (i:Industry {id: $id})
    DETACH DELETE i
    """
    nodes_deleted = await neo4j_client.run_query_consume(query, {"id": industry_id})
    if nodes_deleted == 0:
        raise HTTPException(status_code=404, detail="Industry не найдена")
    return {"detail": f"Industry {industry_id} удалена"}
