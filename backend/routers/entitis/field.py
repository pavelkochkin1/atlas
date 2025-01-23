import uuid
from typing import List

from db.neo4j_client import Neo4jClient, get_neo4j_client
from fastapi import APIRouter, Depends, HTTPException
from schemas.field import FieldCreate, FieldRead

fields_router = APIRouter(prefix="/fields")


@fields_router.post("/", response_model=FieldRead)
async def create_field(field_in: FieldCreate, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    _id = str(uuid.uuid4())
    query = """
    CREATE (f:Field {id: $id, name: $name, description: $description})
    RETURN f.id as id, f.name as name, f.description as description
    """
    result = await neo4j_client.run_query_single(
        query,
        {"id": _id, "name": field_in.name, "description": field_in.description},
    )
    if not result:
        raise HTTPException(status_code=400, detail="Ошибка создания Field")
    return FieldRead(id=result.get("id"), name=result.get("name"), description=result.get("description"))


@fields_router.get("/", response_model=List[FieldRead])
async def get_fields(neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = "MATCH (f:Field) RETURN f.id AS id, f.name AS name, f.description AS description"
    results = await neo4j_client.run_query_all(query)
    return [FieldRead(id=r["id"], name=r["name"], description=r["description"]) for r in results]


@fields_router.get("/{field_id}", response_model=FieldRead)
async def get_field(field_id: str, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (f:Field {id: $id})
    RETURN f.id AS id, f.name AS name, f.description AS description
    """
    record = await neo4j_client.run_query_single(query, {"id": field_id})
    if not record:
        raise HTTPException(status_code=404, detail="Field не найден")
    return FieldRead(id=record.get("id"), name=record.get("name"), description=record.get("description"))


@fields_router.put("/{field_id}", response_model=FieldRead)
async def update_field(field_id: str, field_in: FieldCreate, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (f:Field {id: $id})
    SET f.name = $name, f.description = $description
    RETURN f.id AS id, f.name AS name, f.description AS description
    """
    record = await neo4j_client.run_query_single(
        query, {"id": field_id, "name": field_in.name, "description": field_in.description}
    )
    if not record:
        raise HTTPException(status_code=404, detail="Field не найден или ошибка при обновлении")
    return FieldRead(
        id=record.get("id"),
        name=record.get("name"),
        description=record.get("description"),
    )


@fields_router.delete("/{field_id}")
async def delete_field(field_id: str, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (f:Field {id: $id})
    DELETE f
    """
    nodes_deleted = await neo4j_client.run_query_consume(query, {"id": field_id})
    if nodes_deleted == 0:
        raise HTTPException(status_code=404, detail="Field не найден или ошибка при удалении")
    return {"detail": f"Field {field_id} удален"}
