import pandas as pd
from neo4j import GraphDatabase


URI = "bolt://localhost:7687"  
AUTH = ("neo4j", "pwd123qaz")
df = pd.read_csv("/mnt/cgshare/triples.csv")

def create_knowledge_graph(driver, dataframe):
    with driver.session() as session:
        try:
            session.run("CREATE CONSTRAINT ON (p:person) ASSERT p.name IS UNIQUE")
        except Exception as e:
            print(f"create error: {e}")


    with driver.session() as session:
        for index, row in dataframe.iterrows():
            head = row['head']
            tail = row['tail']
            label = row['label']

            cypher_query = f"""
            MERGE (h:person {{name: $head}})
            MERGE (t:person {{name: $tail}})
            MERGE (h)-[:`{label}`]->(t)
            """
            
            session.run(cypher_query, head=head, tail=tail)
        print("Done!")

if __name__ == "__main__":
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        create_knowledge_graph(driver, df)