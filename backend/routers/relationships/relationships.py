from db.neo4j_client import Neo4jClient, get_neo4j_client
from fastapi import APIRouter, Depends, HTTPException
from schemas.relationships import (
    AddFieldRequest,
    BelongsToIndustryRequest,
    BelongsToTeamRequest,
    FieldReferencesRequest,
    HasResponsibleRequest,
    MaintainedByRequest,
    PartOfRequest,
    SourceOfRequest,
)

relationships_router = APIRouter()


@relationships_router.post("/table/add_field")
async def add_field_to_table(request: AddFieldRequest, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    """
    Создаём связь (Table)-[:HAS_FIELD]->(Field).
    """
    query = """
    MATCH (t:Table {name: $table_name}), (f:Field {id: $field_id})
    CREATE (t)-[:HAS_FIELD]->(f)
    """
    created_cnt = await neo4j_client.create_relationship(query, request.dict())
    if created_cnt == 0:
        raise HTTPException(status_code=404, detail="Table или Field не найдены, либо связь уже существует")
    return {"detail": f"Связь (Table {request.table_name})-[:HAS_FIELD]->(Field {request.field_id}) создана"}


@relationships_router.post("/table/source_of")
async def table_source_of_table(request: SourceOfRequest, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    """
    Создаём связь (Table)-[:SOURCE_OF]->(Table).
    """
    query = """
    MATCH (s:Table {name: $source_name}), (t:Table {name: $target_name})
    CREATE (s)-[:SOURCE_OF]->(t)
    """
    created_cnt = await neo4j_client.create_relationship(query, request.dict())
    if created_cnt == 0:
        raise HTTPException(status_code=404, detail="Исходная или целевая Table не найдены, либо связь уже существует")
    return {"detail": f"Связь (Table {request.source_name})-[:SOURCE_OF]->(Table {request.target_name}) создана"}


@relationships_router.post("/table/belongs_to")
async def table_belongs_to_industry(
    request: BelongsToIndustryRequest, neo4j_client: Neo4jClient = Depends(get_neo4j_client)
):
    """
    Создаём связь (Table)-[:BELONGS_TO]->(Industry).
    """
    query = """
    MATCH (t:Table {name: $table_name}), (i:Industry {id: $industry_id})
    CREATE (t)-[:BELONGS_TO]->(i)
    """
    created_cnt = await neo4j_client.create_relationship(query, request.dict())
    if created_cnt == 0:
        raise HTTPException(status_code=404, detail="Таблица или Индустрия не найдены, либо связь уже существует")
    return {"detail": "Связь (Table)-[:BELONGS_TO]->(Industry) создана"}


@relationships_router.post("/table/maintained_by")
async def table_maintained_by_team(request: MaintainedByRequest, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    """
    Создаём связь (Table)-[:MAINTAINED_BY]->(Team).
    """
    query = """
    MATCH (t:Table {name: $table_name}), (tm:Team {id: $team_id})
    CREATE (t)-[:MAINTAINED_BY]->(tm)
    """
    created_cnt = await neo4j_client.create_relationship(query, request.dict())
    if created_cnt == 0:
        raise HTTPException(status_code=404, detail="Таблица или Команда не найдены, либо связь уже существует")
    return {"detail": "Связь (Table)-[:MAINTAINED_BY]->(Team) создана"}


@relationships_router.post("/table/has_responsible")
async def table_has_responsible(request: HasResponsibleRequest, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    """
    Создаём связь (Table)-[:HAS_RESPONSIBLE]->(Person).
    """
    query = """
    MATCH (t:Table {name: $table_name}), (p:Person {email: $person_email})
    CREATE (t)-[:HAS_RESPONSIBLE]->(p)
    """
    print(request)
    params = {"table_name": request.table_name, "person_email": request.person_email}
    created_cnt = await neo4j_client.create_relationship(query, params)
    if created_cnt == 0:
        raise HTTPException(status_code=404, detail="Таблица или Человек не найдены, либо связь уже существует")
    return {"detail": "Связь (Table)-[:HAS_RESPONSIBLE]->(Person) создана"}


@relationships_router.post("/table/part_of")
async def table_part_of_semantic_block(request: PartOfRequest, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    """
    Создаём связь (Table)-[:PART_OF]->(SemanticBlock).
    """
    query = """
    MATCH (t:Table {name: $table_name}), (b:SemanticBlock {id: $block_id})
    CREATE (t)-[:PART_OF]->(b)
    """
    created_cnt = await neo4j_client.create_relationship(query, request.dict())
    if created_cnt == 0:
        raise HTTPException(status_code=404, detail="Таблица или SemanticBlock не найдены, либо связь уже существует")
    return {"detail": "Связь (Table)-[:PART_OF]->(SemanticBlock) создана"}


@relationships_router.post("/person/belongs_to")
async def person_belongs_to_team(request: BelongsToTeamRequest, neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    """
    Создаём связь (Person)-[:BELONGS_TO]->(Team).
    """
    query = """
    MATCH (p:Person {email: $email}), (tm:Team {id: $team_id})
    CREATE (p)-[:BELONGS_TO]->(tm)
    """
    created_cnt = await neo4j_client.create_relationship(query, request.dict())
    if created_cnt == 0:
        raise HTTPException(status_code=404, detail="Person или Team не найдены, либо связь уже существует")
    return {"detail": "Связь (Person)-[:BELONGS_TO]->(Team) создана"}


@relationships_router.post("/field/references")
async def field_references_field(
    request: FieldReferencesRequest, neo4j_client: Neo4jClient = Depends(get_neo4j_client)
):
    """
    Создаём связь (Field)-[:REFERENCES]->(Field).
    """
    query = """
    MATCH (f1:Field {id: $field_id}), (f2:Field {id: $ref_field_id})
    CREATE (f1)-[:REFERENCES]->(f2)
    """
    created_cnt = await neo4j_client.create_relationship(query, request.dict())
    if created_cnt == 0:
        raise HTTPException(status_code=404, detail="Field(ы) не найдены, либо связь уже существует")
    return {"detail": "Связь (Field)-[:REFERENCES]->(Field) создана"}
