# DBMS_PROJECT

## To initialize Aura DB database:
Create your own instance. A credential file will be downloaded. Save it in the Data folder.
You can directly use product_new and copurchase_new to directly create nodes and relationship in AuraDB (Using cypher queries/python driver takes a very long time. In AuraDB it is instantaneous.)

Use product_new file as the nodes with id as primary key and copurchase as relationship 

### app.ipynb
Python driver file. Also segregates first 87000 products and relationships into two csv files product_new.csv and copurchase_new.csv

In URL, put your Neo4jd database URL with `neo4j+ssc` form instead of `neo4j+s`

## Code

### json_to_csv.py:
contains code to convert input json file (here Data/data.json) to products.csv and categories.csv 

### app2.py
driver file for neo4js and flask website
 ```bash
      python app2.py
 ```

## Outputs

Contains products.csv and categories.csv
Also contains neo4j model developed, to convert this csv files to graph database in neo4j.
To utilise this zip file, set up an instance of neo4j Aura DB, go to Import tab, and select Open model (with data) option. 
Explore, have fun.
