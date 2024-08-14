from neo4j import GraphDatabase
import asyncio

async def save_graph_async(driver, graph_query):
    try:
        async def execute_query(tx, query):
            result = await tx.run(query)
            return await result.consume()

        async with driver.session() as session:
            await session.execute_write(execute_query, graph_query)
        print("Data written to Neo4j database successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

def close_driver(driver):
    driver.close()