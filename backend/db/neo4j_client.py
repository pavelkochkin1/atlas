from typing import Any, List

from core.config import settings
from neo4j import AsyncGraphDatabase


class Neo4jClient:
    def __init__(self):
        self.driver = AsyncGraphDatabase.driver(
            uri=f"bolt://{settings.NEO4J_HOST}:{settings.NEO4j_PORT}",
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )

    async def close(self):
        await self.driver.close()

    async def run_query_single(self, query: str, parameters: dict = None) -> Any:
        async with self.driver.session() as session:
            result = await session.run(query, parameters)
            return await result.single()

    async def run_query_all(self, query: str, parameters: dict = None) -> List[Any]:
        async with self.driver.session() as session:
            result = await session.run(query, parameters)
            return [record async for record in result]

    async def run_query_consume(self, query: str, parameters: dict = None) -> int:
        async with self.driver.session() as session:
            result = await session.run(query, parameters)
            summary = await result.consume()
            return summary.counters.nodes_deleted

    async def create_relationship(self, query: str, parameters: dict = None) -> Any:
        async with self.driver.session() as session:
            result = await session.run(query, parameters)
            summary = await result.consume()
            return summary.counters.relationships_created


def get_neo4j_client():
    return Neo4jClient()
