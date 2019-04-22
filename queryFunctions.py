# pip install neo4j-driver
# https://neo4j.com/docs/api/python-driver/current/
from neo4j.v1 import GraphDatabase, basic_auth

def pickwine(variety, country, region, winery, price):
        prices = price.split(" to ")
        lower = int(prices[0])
        upper = int(prices[1])
        # query by current selection
        driver = GraphDatabase.driver(
            "bolt://localhost:7687", 
            auth=basic_auth("neo4j", "jesus"))
        session = driver.session()

        # 1 - Wine Variety
        # 2 - Country
        # 3 - Region
        # 4 - Winery
        # 5 - Price range
        cypher_query = '''
        MATCH (z:Winery)-[:MAKES]->(w:Wine)<-[d:DESCRIBES]-(r:Reviewer)
        WHERE z.wineryName = $winery AND w.variety = $variety AND
        z.country = $country AND z.region_1 = $region AND
        toInteger(w.price) >= $lower AND toInteger(w.price) <= $upper
        WITH w.variety as wine, z.wineryName as winery, w.price as price, z.country as country, z.region_1 as region
        RETURN wine, winery, price, country, region
        '''

        results = session.run(cypher_query,
        parameters={"country": country, "region": region, "winery": winery, "variety": variety, "lower": lower, "upper": upper})
        
        wineries = list()
        countries = list()
        regions = list()
        wines = list()
        prices = list()

        for record in results:
            wineries.append(record["winery"])
            countries.append(record["country"])
            regions.append(record["region"])
            wines.append(record["wine"])
            prices.append(record["price"])

        if len(wineries) == 0:
            wineries.append("None Found")
            countries.append("None Found")
            regions.append("None Found")
            wines.append("None Found")
            prices.append("None Found")
        records = {"wineries": wineries, "countries", countries, "regions": regions, "wines": wines, "prices": prices}

        return records


def wineryDistance(wine, lowerHop, higherHop):
  driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=basic_auth("neo4j", "jesus"))
  session = driver.session()

  cypher_query:'''
  MATCH (w:Wine)-[:MAKES*$lower..$upper]-(h:Wine)
  WHERE w.variety = $variety
  WITH h.variety = wine
  RETURN DISTINCT wine
  '''

  results = session.run(cypher_query,
        parameters={"variety": wine, "lower": lowerHop, "upper": upperHop})

  wines = list()

  for record in results:
    wines.append(record["wine"])

  if len(wines) == 0:
    wines.append("None Found")

  return wines

def reviewerDistance(wine, lowerHop, higherHop):
  driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=basic_auth("neo4j", "jesus"))
  session = driver.session()

  cypher_query:'''
  MATCH (w:Wine)-[:DESCRIBES*$lower..$upper]-(h:Wine)
  WHERE w.variety = $variety
  WITH h.variety = wine
  RETURN DISTINCT wine
  '''

  results = session.run(cypher_query,
        parameters={"variety": wine, "lower": lowerHop, "upper": upperHop})

  wines = list()

  for record in results:
    wines.append(record["wine"])

  if len(wines) == 0:
    wines.append("None Found")

  return wines


