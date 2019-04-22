# pip install neo4j-driver
# https://neo4j.com/docs/api/python-driver/current/
from neo4j.v1 import GraphDatabase, basic_auth


# Below is example code from Trumpworld
# Bolt takes IP address and bolt port listed on site
# auth takes username and password listed on site
driver = GraphDatabase.driver(
    "bolt://localhost:7687", 
    auth=basic_auth("neo4j", "jesus"))
session = driver.session()

# What are all the Organizations in Trumpworld?
cypher_query = '''
MATCH (w:Wine)
RETURN w.variety AS name LIMIT $limit
'''

results = session.run(cypher_query,
  parameters={"limit": 10})

for record in results:
  print(record['name'])
