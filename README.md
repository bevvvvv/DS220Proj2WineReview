# DS220Proj2WineReview

## Insertion of Data to Neo4j DB

1. Run the createNodes.r r script using the command `Rscript createNodes.r` if you have R installed. You may need to edit the parameters of a line to change how many of the 130k lines are being used.
2. Move the new csv files that have been created to the import folder underneath the installation of neo4j on your machine.
3. Start your neo4j database by executing the command `neo4j console` from the neo4j bin directory.
4. Run import_csv.cypher and then import_csv_part2.cypher by piping the contents of the file (using cat or type on windows) into the cypher shell command (which exists in the neo4j bin). You may need to add credentials which can be set from the neo4j browser.
5. Check imported data with `MATCH (n) RETURN n` or other cypher commands and delete current graph with `MATCH (n) DETACH DELETE n`

Please note that if you are inserting a large amount of rows you may need to wait for indexing to occur to create the relationships in a timely manner.

## Running Django Python web framework

1. Install django on your system via `pip install django`
2. You can confirm an installation by running `python -m django --version` (most recent 2.2)
3. Navigate to the git respository directory
4. Run `python manage.py runserver`
5. You can then access the UI via http://127.0.0.1:8000/polls/



