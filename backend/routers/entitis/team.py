from typing import List

from db.neo4j_client import Neo4jClient, get_neo4j_client
from fastapi import APIRouter, Depends, HTTPException
from schemas.team import Team

team_router = APIRouter(prefix="/teams")


@team_router.post("/", response_model=Team)
async def create_team(team_in: Team, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    CREATE (t:Team {id: $id, name: $name})
    RETURN t.id as id, t.name as name
    """
    result = await neo4j_client.run_query_single(query, {"id": team_in.id, "name": team_in.name})
    if not result:
        raise HTTPException(status_code=400, detail="Ошибка создания Team")
    return Team(id=result.get("id"), name=result.get("name"))


@team_router.get("/", response_model=List[Team])
async def get_teams(neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = "MATCH (t:Team) RETURN t.id AS id, t.name AS name"
    results = await neo4j_client.run_query_all(query)
    return [Team(id=r["id"], name=r["name"]) for r in results]


@team_router.get("/{team_id}", response_model=Team)
async def get_team(team_id: str, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (t:Team {id: $id})
    RETURN t.id AS id, t.name AS name
    """
    record = await neo4j_client.run_query_single(query, {"id": team_id})
    if not record:
        raise HTTPException(status_code=404, detail="Team не найдена")
    return Team(
        id=record.get("id"),
        name=record.get("name"),
    )


@team_router.put("/{team_id}", response_model=Team)
async def update_team(team_id: str, team_in: Team, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (t:Team {id: $id})
    SET t.name = $name
    RETURN t.id AS id, t.name AS name
    """
    record = await neo4j_client.run_query_single(query, {"id": team_id, "name": team_in.name})
    if not record:
        raise HTTPException(status_code=404, detail="Team не найдена или ошибка при обновлении")
    return Team(
        id=record.get("id"),
        name=record.get("name"),
    )


@team_router.delete("/{team_id}")
async def delete_team(team_id: str, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (t:Team {id: $id})
    DETACH DELETE t
    """
    nodes_deleted = await neo4j_client.run_query_consume(query, {"id": team_id})
    if nodes_deleted == 0:
        raise HTTPException(status_code=404, detail="Team не найдена")
    return {"detail": f"Team {team_id} удалена"}
