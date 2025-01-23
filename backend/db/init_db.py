import asyncio

from db.neo4j_client import get_neo4j_client


async def init_db():
    neo4j = get_neo4j_client()
    people = [
        {"email": "weasley@mts.ru", "first_name": "Ron", "last_name": "Weasley"},
        {"email": "rickman@mts.ru", "first_name": "Alan", "last_name": "Rickman"},
        {"email": "granger@mts.ru", "first_name": "Hermione", "last_name": "Granger"},
        {"email": "potter@mts.ru", "first_name": "Harry", "last_name": "Potter"},
        {"email": "kochkin@mts.ru", "first_name": "Pavel", "last_name": "Kochkin"},
        {"email": "shatrov@mts.ru", "first_name": "Oleg", "last_name": "Shatrov"},
    ]

    industries = [
        {"id": "GR", "name": "Golden Record"},
        {"id": "kion", "name": "KION"},
        {"id": "strocki", "name": "STROCKI"},
    ]

    teams = [
        {"id": "PML", "name": "Person Modeling Lab"},
        {"id": "CP", "name": "Customer Profile"},
        {"id": "KA", "name": "Kion Analytics"},
        {"id": "SA", "name": "Strocki Analytics"},
    ]

    # 1. MERGE для Person
    for p in people:
        query = """
        MERGE (person:Person {email: $email})
        SET person.first_name = $first_name,
            person.last_name  = $last_name
        """
        await neo4j.run_query_consume(query, p)

    # 2. MERGE для Industry
    for i in industries:
        query = """
        MERGE (ind:Industry {id: $id})
        SET ind.name = $name
        """
        await neo4j.run_query_consume(query, i)

    # 3. MERGE для Team
    for t in teams:
        query = """
        MERGE (team:Team {id: $id})
        SET team.name = $name
        """
        await neo4j.run_query_consume(query, t)

    await neo4j.close()
    print("Инициализация данных в Neo4j завершена успешно.")


if __name__ == "__main__":
    asyncio.run(init_db())
