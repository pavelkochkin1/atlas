from typing import List

from db.neo4j_client import Neo4jClient, get_neo4j_client
from fastapi import APIRouter, Depends, HTTPException
from schemas.person import Person

person_router = APIRouter(prefix="/persons")


@person_router.post("/", response_model=Person)
async def create_person(person_in: Person, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    CREATE (p:Person {first_name: $first_name, last_name: $last_name, email: $email})
    RETURN p.id AS id, p.first_name AS first_name, p.last_name AS last_name, p.email AS email
    """
    result = await neo4j_client.run_query_single(
        query,
        {
            "first_name": person_in.first_name,
            "last_name": person_in.last_name,
            "email": person_in.email,
        },
    )
    if not result:
        raise HTTPException(status_code=400, detail="Ошибка создания Person")
    return Person(
        first_name=result.get("first_name"),
        last_name=result.get("last_name"),
        email=result.get("email"),
    )


@person_router.get("/", response_model=List[Person])
async def get_persons(neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = "MATCH (p:Person) RETURN p.id AS id, p.first_name AS first_name, p.last_name AS last_name, p.email AS email"
    results = await neo4j_client.run_query_all(query)
    return [
        Person(
            first_name=r["first_name"],
            last_name=r["last_name"],
            email=r["email"],
        )
        for r in results
    ]


@person_router.get("/{email}", response_model=Person)
async def get_person(email: str, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (p:Person {email: $email})
    RETURN p.id AS id, p.first_name AS first_name, p.last_name AS last_name, p.email AS email
    """
    record = await neo4j_client.run_query_single(query, {"email": email})
    if not record:
        raise HTTPException(status_code=404, detail="Person не найдена")
    return Person(
        first_name=record.get("first_name"),
        last_name=record.get("last_name"),
        email=record.get("email"),
    )


@person_router.put("/{email}", response_model=Person)
async def update_person(email: str, person_in: Person, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (p:Person {email: $new_email})
    SET p.first_name = $first_name, p.last_name = $last_name, p.email = $email
    RETURN p.id AS id, p.first_name AS first_name, p.last_name AS last_name, p.email AS email
    """
    record = await neo4j_client.run_query_single(
        query,
        {
            "new_email": person_in.email,
            "first_name": person_in.first_name,
            "last_name": person_in.last_name,
            "email": email,
        },
    )
    if not record:
        raise HTTPException(status_code=404, detail="Person не найдена или ошибка при обновлении")
    return Person(
        first_name=record.get("first_name"),
        last_name=record.get("last_name"),
        email=record.get("email"),
    )


@person_router.delete("/{email}")
async def delete_person(email: str, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    query = """
    MATCH (p:Person {email: $email})
    DETACH DELETE p
    """
    nodes_deleted = await neo4j_client.run_query_consume(query, {"email": email})
    if nodes_deleted == 0:
        raise HTTPException(status_code=404, detail="Person не найдена")
    return {"detail": f"Person {email} удалена"}
