# pip install neo4j-driver
# https://neo4j.com/docs/api/python-driver/current/
from neo4j.v1 import GraphDatabase, basic_auth

# Below is example code from Trumpworld
driver = GraphDatabase.driver(
    "bolt://100.26.228.61:33188", 
    auth=basic_auth("neo4j", "destruction-cries-majorities"))
session = driver.session()

# What are all the Organizations in Trumpworld?
cypher_query = '''
MATCH (o:Organization)
RETURN o.name AS name LIMIT $limit
'''

results = session.run(cypher_query,
  parameters={"limit": 10})

for record in results:
  print(record['name'])
