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
        records = {"wineries": wineries, "countries", countries, "regions": regions, "wines": wines, "prices": prices}

        return records


