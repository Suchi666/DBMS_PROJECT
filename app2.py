from flask import Flask,render_template, request, redirect, url_for, session,send_file
from neo4j import GraphDatabase
import dotenv
import os
import numpy as np
import pandas as pd
import re

app = Flask(__name__)
#from app import routes, models
 
app.secret_key = 'your secret key'

load_status = dotenv.load_dotenv("Data/Neo4j-34704290-Created-2024-04-14.txt")       # replace by your neo4j AuraDB credential txt file
if load_status is False:
    raise RuntimeError('Environment variables not loaded.')

URI =  "neo4j+ssc://34704290.databases.neo4j.io"            #here use neo4j+ssc
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
print(URI,AUTH)
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

# cypher_query = (
#     "MATCH (n:Product) RETURN n LIMIT 5;"
# )

# Define a function to execute the query and process the result
def process_result(tx, cypher_query,variable):
    result = tx.run(cypher_query)
    similar_products=[record[variable] for record in result]
    return similar_products

# Execute the Cypher query within a session
def execute_query(query,variable):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session(database="neo4j") as session:
            similar_products = session.execute_write(process_result,query,variable)
            return similar_products
        
def process_result2(tx, cypher_query,variable,search_term,tag):
    result = tx.run(cypher_query,search_term=search_term)
    similar_products=[record[variable] for record in result]
    return similar_products

# Execute the Cypher query within a session
def execute_query2(query,variable,search_term,tag):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session(database="neo4j") as session:
            similar_products = session.execute_write(process_result2,query,variable,search_term,tag)
            return similar_products


# Process the similar products
# print("Product list : ")
# for product in similar_products:
#     print(product['title'])

@app.route('/')
def hello():
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
 
    cypher_query=(
    "MATCH (n:Product) RETURN n;"
    )
    ans=execute_query(cypher_query,"n")
    
    
    groups=[]
    data=[]
    for each_ans in ans:
        groups.append(each_ans['group'])
    groups=set(groups)
    print("Groups........")
    print(groups)
    return render_template('dashboard_mentee.html',groups=groups,selected_filter='none',data=data)



    
 
    

    
    cursor.execute('SELECT * FROM tag')  
    tags = cursor.fetchall()
    return render_template("dashboard_mentee.html",mentee=mentee,tags=tags,selected_filter = 'none')

def extract_titles(data):
    for entry in data:
        for each_entry in entry:
            print(each_entry)
            for each_node in each_entry:
                print("Each node.....")
                print(each_node)
    return 0
    

    



@app.route('/search_sort_filter', methods=['POST'])
def search_sort_filter():
    cypher_query=(
    "MATCH (n:Product) RETURN n;"
    )
    ans=execute_query(cypher_query,"n")
    
    
    groups=[]
    all_titles=[]
    all_sales=[]
    all_ASIN=[]
   
    for each_ans in ans:
        groups.append(each_ans['group'])
    groups=set(groups)
    selected_tag=""
    if 'filter' in request.form:
        selected_tag=request.form['filter']
        print(selected_tag)
        search_term = request.form.get('search_term')
        if search_term:
            search_term=str(search_term)
            print(search_term)
            cypher_query="MATCH X=(p1:Product {group : 'Book'})-[:Similar]->(p2:Product) WHERE p1.title STARTS WITH $search_term RETURN X  ORDER BY p1.sales_rank"
            ans=execute_query2(cypher_query,"X",search_term,selected_tag)
            print(ans)
            print("Var new.............")
            for each_entry in ans:
                var_new=str(each_entry)
                pattern = r"title': '([^']+)'"
                titles = re.findall(pattern, var_new)
                sales_rank_pattern = r"'sales_rank': (\d+)"
                ASIN_pattern = r"'ASIN': (\d+)"
                sales_rank = re.findall(sales_rank_pattern, var_new)
                ASIN = re.findall(ASIN_pattern, var_new)

                for each_title in titles:
                    all_titles.append(each_title)
                for each_sales_rank in sales_rank:
                    all_sales.append(int(each_sales_rank))
                for each_ASIN in ASIN:
                    all_ASIN.append(int(each_ASIN))
            

            combined_data = [{'title': title, 'sales_rank': sales, 'ASIN': ASIN} for title, sales, ASIN in zip(all_titles, all_sales, all_ASIN)]
            return render_template('dashboard_mentee.html',groups=groups,selected_filter='none',data=combined_data)
        else:
            cypher_query="MATCH X=(p1:Product {group : 'Book'})-[:Similar]->(p2:Product) RETURN X ORDER BY p1.sales_rank"
            ans=execute_query2(cypher_query,"X","",selected_tag)
        
            print("Var new.............")
            for each_entry in ans:
                var_new=str(each_entry)
                pattern = r"title': '([^']+)'"
                titles = re.findall(pattern, var_new)
                sales_rank_pattern = r"'sales_rank': (\d+)"
                ASIN_pattern = r"'ASIN': (\d+)"
                sales_rank = re.findall(sales_rank_pattern, var_new)
                ASIN = re.findall(ASIN_pattern, var_new)

                for each_title in titles:
                    all_titles.append(each_title)
                for each_sales_rank in sales_rank:
                    all_sales.append(int(each_sales_rank))
                for each_ASIN in ASIN:
                    all_ASIN.append(int(each_ASIN))

                combined_data = [{'title': title, 'sales_rank': sales, 'ASIN': ASIN} for title, sales, ASIN in zip(all_titles, all_sales, all_ASIN)]
                


# Print the extracted titles
            print(all_titles)
            #print(var_new)
        #titles = extract_titles(ans)
        #print(titles)
        
    return render_template('dashboard_mentee.html',groups=groups,selected_filter='none',data=combined_data)


@app.route('/payment', methods=['GET','POST'])
def payment():
    if request.method=='POST':
        return redirect(url_for("dashboard"))
    return render_template('payment.html',)

    

#     parameters = []
#     sort_option = "(SELECT COUNT(*) FROM course_mentee WHERE course_mentee.course_id = course.course_id) DESC"
#     query = "SELECT course.*, mentor.mentor_name FROM course JOIN mentor ON course.mentor_id = mentor.mentor_id"
#     sort_choice = request.form['sort']

#     if 'sort' in request.form:
#         if sort_choice == 'valuation':
#             sort_option = "(SELECT COUNT(*) FROM course_mentee WHERE course_mentee.course_id = course.course_id) DESC"
#         elif sort_choice == 'equity':
#             sort_option = "course_price ASC"
#         elif sort_choice == 'investment':
#             sort_option = "course_price DESC"

#     selected_tag = request.form['filter']
#     if 'filter' in request.form:
#         if selected_tag != 'none':
#             query += " JOIN course_tag_relation ON course.course_id = course_tag_relation.course_id"
#             query += " JOIN tag ON course_tag_relation.tag_id = tag.tag_id"
#             query += " WHERE tag.tag_name = %s AND course.course_status='verified'"
#             parameters.append(selected_tag)
#         else:
#             query += " WHERE 1=1 AND course.course_status='verified'"

#     else:
#         query += " WHERE 1=1 AND course.course_status='verified'"  # Ensuring the WHERE clause is present even if no tag is selected

#     search_term = request.form.get('search_term')
#     search_type = request.form.get('search_type')

#     if search_term:

#         if search_type == 'mentor':
#             query += " AND mentor.mentor_name LIKE %s"
#         elif search_type == 'course':
#             query += " AND course.course_name LIKE %s"
#         parameters.append("%" + search_term + "%")

#     query += f" ORDER BY {sort_option}"


#     cursor.execute(query, parameters)

    
#     print(selected_tag)
#     cursor.execute(query, parameters)
#     data = cursor.fetchall()
#     # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#     #     return jsonify(data=data,tag=tag)  # Return JSON response for AJAX request
#     # else:
#     return render_template('dashboard_mentee.html',mentee=mentee, data=data, tags=tag, selected_filter=selected_tag, sort_option=sort_choice, search_term=search_term, search_type=search_type)


if __name__ == '__main__':
    app.run(debug=True)