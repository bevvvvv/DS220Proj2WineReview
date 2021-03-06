# pip install neo4j-driver
# https://neo4j.com/docs/api/python-driver/current/
from neo4j.v1 import GraphDatabase, basic_auth

def pickwine(variety, country, region, winery, price, score, params):
  prices = price.split(" to ")
  lower = int(prices[0])
  upper = int(prices[1])

  scores = score.split(" to ")
  lowScore = int(scores[0])
  highScore = int(scores[0])
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
  WHERE
  '''

  for i in range(len(params)):
    if i > 0:
      cypher_query = cypher_query + ' AND '
    if params[i] == "variety":
      cypher_query = cypher_query + 'w.variety = $variety'
    elif params[i] == "country":
      cypher_query = cypher_query + 'z.country = $country '
    elif params[i] == "region":
      cypher_query = cypher_query + 'z.region_1 = $region'
    elif params[i] == "winery":
      cypher_query = cypher_query + 'z.wineryName = $winery'
    elif params[i] == "price":
      cypher_query = cypher_query + 'toInteger(w.price) >= $lower AND toInteger(w.price) <= $upper'
    elif params[i] == "score":
      cypher_query = cypher_query + 'toInteger(d.points) >= $lowScore AND toInteger(d.points) <= $high'


  cypher_query = cypher_query + '''
  WITH w.variety as wine, z.wineryName as winery, w.price as price, z.country as country, z.region_1 as region, d.points as score, r.reviewerName as reviewer, d.description as description
  RETURN wine, winery, price, country, region, score, reviewer, description LIMIT 50
  '''

  results = session.run(cypher_query,
  parameters={"country": country, "region": region, "winery": winery, "variety": variety, "lower": lower, "upper": upper, "lowScore": lowScore, "high": highScore})
  
  wineries = list()
  countries = list()
  regions = list()
  wines = list()
  prices = list()
  scores = list()
  reviewers = list()
  descriptions = list()

  for record in results:
      wineries.append(record["winery"])
      countries.append(record["country"])
      regions.append(record["region"])
      wines.append(record["wine"])
      prices.append(record["price"])
      scores.append(record["score"])
      reviewers.append(record["reviewer"])
      descriptions.append(record["description"])

  if len(wineries) == 0:
      wineries.append("None Found")
      countries.append("None Found")
      regions.append("None Found")
      wines.append("None Found")
      prices.append("None Found")
      scores.append("None Found")
      reviewers.append("None Found")
      descriptions.append("None Found")

  records = {"wineries": wineries, "countries": countries, "regions": regions, "wines": wines, "prices": prices, "scores": scores, "reviewers": reviewers, "descriptions": descriptions}

  return records


def wineryDistance(wine, lowerHop, higherHop):
  driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=basic_auth("neo4j", "jesus"))
  session = driver.session()

  cypher_query = '''
  MATCH (w:Wine)-[:MAKES*
  '''+ str(lowerHop) + '..' +str(higherHop) + '''
  ]-(h:Wine)<-[:MAKES]-(z:Winery)
  WHERE w.variety = $variety
  WITH h.variety as wine, h.price as price, z.wineryName as winery, z.country as country, z.region_1 as region
  RETURN DISTINCT wine, price, winery, country, region LIMIT 50
  ''' 

  results = session.run(cypher_query,
        parameters={"variety": wine, "lower": lowerHop, "upper": higherHop})

  wineries = list()
  countries = list()
  regions = list()
  wines = list()
  prices = list()
  scores = list()
  reviewers = list()
  descriptions = list()

  for record in results:
    wines.append(record["wine"])
    wineries.append(record["winery"])
    countries.append(record["country"])
    regions.append(record["region"])
    prices.append(record["price"])
    scores.append("NA")
    reviewers.append("NA")
    descriptions.append("NA")

  if len(wines) == 0:
    wineries.append("None Found")
    countries.append("None Found")
    regions.append("None Found")
    wines.append("None Found")
    prices.append("None Found")
    scores.append("None Found")
    reviewers.append("None Found")
    descriptions.append("None Found")

  records = {"wineries": wineries, "countries": countries, "regions": regions, "wines": wines, "prices": prices, "scores": scores, "reviewers": reviewers, "descriptions": descriptions}

  return records

def reviewerDistance(wine, lowerHop, higherHop):
  driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=basic_auth("neo4j", "jesus"))
  session = driver.session()

  cypher_query = '''
  MATCH (w:Wine)-[:DESCRIBES*
  '''+ str(lowerHop) + '..' +str(higherHop) + '''
  ]-(h:Wine)<-[d:DESCRIBES]-(r:Reviewer)
  WHERE w.variety = $variety
  WITH h.variety as wine, h.price as price, r.reviewerName as reviewer, d.points as score, d.description as description
  RETURN DISTINCT wine, price, reviewer, score, description LIMIT 50
  '''

  results = session.run(cypher_query,
        parameters={"variety": wine, "lower": lowerHop, "upper": higherHop})

  wineries = list()
  countries = list()
  regions = list()
  wines = list()
  prices = list()
  scores = list()
  reviewers = list()
  descriptions = list()

  for record in results:
    wines.append(record["wine"])
    wineries.append("NA")
    countries.append("NA")
    regions.append("NA")
    prices.append(record["price"])
    scores.append(record["score"])
    reviewers.append(record["reviewer"])
    descriptions.append(record["description"])

  if len(wines) == 0:
    wines.append("None Found")
    wineries.append("None Found")
    countries.append("None Found")
    regions.append("None Found")
    prices.append("None Found")
    scores.append("None Found")
    reviewers.append("None Found")
    descriptions.append("None Found")

  records = {"wineries": wineries, "countries": countries, "regions": regions, "wines": wines, "prices": prices, "scores": scores, "reviewers": reviewers, "descriptions": descriptions}

  return records


