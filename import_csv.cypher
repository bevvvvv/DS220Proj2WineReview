// Create wines
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:wines.csv" AS row
CREATE (:Wine {variety: row.variety, price: row.price});

// Create wineries
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:wineries.csv" AS row
CREATE (:Winery {wineryName: row.winery, region_1: row.region_1, region_2: row.region_2, province: row.province, designation, row.designation, country: row.country});

// Create reviews
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:reviews.csv" AS row
CREATE (:Review {title: row.title, points: row.points, description, row.description});

// Create reviewers
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:reviewers.csv" AS row
CREATE (:Reviewer {reviewerName: row.taster_name,  twitter: row.taster_twitter_handle});


CREATE INDEX ON :Wine(variety);
CREATE INDEX ON :Winery(wineryName);
CREATE INDEX ON :Review(title);
CREATE INDEX ON :Reveiwer(reviewerName);

schema await

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:wineries.csv" AS row
MATCH (winery:Winery {wineryName: row.winery})
MATCH (wine:Wine {variety: row.variety})
MERGE (winery)-[:MAKES]->(wine);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:reveiwers.csv" AS row
MATCH (reviewer:Reviewer {reviewerName: row.taster_name})
MATCH (review:Review {title: row.title})
MERGE (reviewer)-[:WROTE]->(review);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:reviews.csv" AS row
MATCH (review:Review {title: row.title})
MATCH (wine:Wine {variety: row.variety})
MERGE (review)-[:DESCRIBES]->(wine);
