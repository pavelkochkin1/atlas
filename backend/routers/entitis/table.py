from typing import List

from db.neo4j_client import Neo4jClient, get_neo4j_client
from fastapi import APIRouter, Depends, HTTPException
from schemas.table import Table

table_router = APIRouter(prefix="/tables")


@table_router.post("/", response_model=Table)
async def create_table(table_in: Table, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    CREATE (t:Table {name: $name, description: $description})
    RETURN t.name as name, t.description as description
    """
    result = await neo4j_client.run_query_single(query, {"name": table_in.name, "description": table_in.description})
    if not result:
        raise HTTPException(status_code=400, detail="Ошибка создания Table")
    return Table(
        name=result.get("name"),
        description=result.get("description"),
    )


@table_router.get("/", response_model=List[Table])
async def get_tables(neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = "MATCH (t:Table) RETURN t.name AS name, t.description AS description"
    results = await neo4j_client.run_query_all(query)
    return [Table(name=r["name"], description=r["description"]) for r in results]


@table_router.get("/{table_name}", response_model=Table)
async def get_table(table_name: str, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (t:Table {name: $name})
    RETURN t.id AS id, t.name AS name, t.description AS description
    """
    record = await neo4j_client.run_query_single(query, {"name": table_name})
    if not record:
        raise HTTPException(status_code=404, detail="Table не найдена")
    return Table(
        name=record.get("name"),
        description=record.get("description"),
    )


@table_router.put("/{table_name}", response_model=Table)
async def update_table(table_name: str, table_in: Table, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (t:Table {name: $name})
    SET t.name = $name, t.description = $description
    RETURN t.id AS id, t.name AS name, t.description AS description
    """
    record = await neo4j_client.run_query_single(query, {"name": table_name, "description": table_in.description})

    if not record:
        raise HTTPException(status_code=404, detail="Table не найдена или ошибка при обновлении")
    return Table(
        name=record.get("name"),
        description=record.get("description"),
    )


@table_router.delete("/{table_name}")
async def delete_table(table_name: str, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (t:Table {name: $name})
    DETACH DELETE t
    """
    nodes_deleted = await neo4j_client.run_query_consume(query, {"name": table_name})
    if nodes_deleted == 0:
        raise HTTPException(status_code=404, detail="Table не найдена")
    return {"detail": f"Table {table_name} удалена"}
