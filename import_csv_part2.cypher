USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///wine.csv" AS row
MATCH (winery:Winery {wineryName: row.winery})
MATCH (wine:Wine {variety: row.variety})
MERGE (winery)-[:MAKES]->(wine);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///reviews.csv" AS row
MATCH (reviewer:Reviewer {reviewerName: row.taster_name})
MATCH (review:Review {title: row.title})
MERGE (reviewer)-[:WROTE]->(review);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///reviews.csv" AS row
MATCH (review:Review {title: row.title})
MATCH (wine:Wine {variety: row.variety})
MERGE (review)-[:DESCRIBES]->(wine);
