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

# 1 - Wine Variety
# 2 - Country
# 3 - Region
# 4 - Winery
# 5 - Price range
cypher_query = '''
MATCH (z:Winery)-[:MAKES]->(w:Wine)<-[d:DESCRIBES]-(r:Reviewer)
WHERE z.wineryName = $winery AND w.variety = $variety AND r.reviewerName = $reviewer
WITH w.variety as wine, z.wineryName as winery, r.reviewerName as reviewer
RETURN wine, winery, reviewer
'''
results = session.run(cypher_query,
  parameters={"winery": "Vega Escal", "variety": "Red Blend", "reviewer": "Roger Voss"})

for record in results:
  print(record['reviewer'])


def pickwine(request):
        var = True
        q1 = request.POST['q1']
        q2 = request.POST['q2']
        q3 = request.POST['q3']
        q4 = request.POST['q4']
        q5 = request.POST['q5']

        prices = q5.split(" to ")
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
        RETURN wine, winery, price, country, region LIMIT 10
        '''

        results = session.run(cypher_query,
        parameters={"country": q2, "region": q3, "winery": q4, "variety": q1, "lower": lower, "upper": upper})
        
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

        return render(request, 'polls/index1.html', {'results':var,'q1':wines[0], 'q2':countries[0], 'q3':regions[0], 'q4':wineries[0],'q5':prices[0]})



