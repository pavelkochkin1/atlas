from typing import List

from db.neo4j_client import Neo4jClient, get_neo4j_client
from fastapi import APIRouter, Depends, HTTPException
from schemas.semantic_block import SemanticBlock

sem_block_router = APIRouter(prefix="/semantic-blocks")


@sem_block_router.post("/", response_model=SemanticBlock)
async def create_semantic_block(block_in: SemanticBlock, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    CREATE (s:SemanticBlock {id: $id, title: $title, content: $content})
    RETURN s.id AS id, s.title AS title, s.content AS content
    """
    result = await neo4j_client.run_query_single(
        query, {"id": block_in.id, "title": block_in.title, "content": block_in.content}
    )
    if not result:
        raise HTTPException(status_code=400, detail="Ошибка создания SemanticBlock")
    return SemanticBlock(
        id=result.get("id"),
        title=result.get("title"),
        content=result.get("content"),
    )


@sem_block_router.get("/", response_model=List[SemanticBlock])
async def get_semantic_blocks(neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = "MATCH (s:SemanticBlock) RETURN s.id AS id, s.title AS title, s.content AS content"
    results = await neo4j_client.run_query_all(query)
    return [SemanticBlock(id=r["id"], title=r["title"], content=r["content"]) for r in results]


@sem_block_router.get("/{block_id}", response_model=SemanticBlock)
async def get_semantic_block(block_id: str, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (s:SemanticBlock {id: $id})
    RETURN s.id AS id, s.title AS title, s.content AS content
    """
    record = await neo4j_client.run_query_single(query, {"id": block_id})
    if not record:
        raise HTTPException(status_code=404, detail="SemanticBlock не найден")
    return SemanticBlock(
        id=record.get("id"),
        title=record.get("title"),
        content=record.get("content"),
    )


@sem_block_router.put("/{block_id}", response_model=SemanticBlock)
async def update_semantic_block(
    block_id: str, block_in: SemanticBlock, neo4j_client: Neo4jClient = Depends(get_neo4j_client)
):
    query = """
    MATCH (s:SemanticBlock {id: $id})
    SET s.title = $title, s.content = $content
    RETURN s.id AS id, s.title AS title, s.content AS content
    """
    record = await neo4j_client.run_query_single(
        query, {"id": block_id, "title": block_in.title, "content": block_in.content}
    )
    if not record:
        raise HTTPException(status_code=404, detail="SemanticBlock не найден или ошибка при обновлении")
    return SemanticBlock(
        id=record.get("id"),
        title=record.get("title"),
        content=record.get("content"),
    )


@sem_block_router.delete("/{block_id}")
async def delete_semantic_block(block_id: str, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (s:SemanticBlock {id: $id})
    DETACH DELETE s
    """
    nodes_deleted = await neo4j_client.run_query_consume(query, {"id": block_id})
    if nodes_deleted == 0:
        raise HTTPException(status_code=404, detail="SemanticBlock не найден")
    return {"detail": f"SemanticBlock {block_id} удален"}
