import json
import csv

def json_to_csv(input_file, products_output_file, categories_output_file):
    with open(input_file, 'r') as json_file:
        data = json.load(json_file)

    # Write to categories.csv
    categories_set = set()
    for entry in data.values():
        for category in entry['categories']:
            categories = category.strip('|').split('|')
            for category_str in categories:
                category_id = category_str.split('[')[-1].rstrip(']')
                category_name = category_str.split('[')[0]
                categories_set.add((category_id, category_name))
    
    with open(categories_output_file, 'w', newline='') as categories_csv:
        categories_writer = csv.writer(categories_csv)
        categories_writer.writerow(['id', 'name'])

        for category_id, category_name in categories_set:
            categories_writer.writerow([category_id, category_name])

    # Write to products.csv
    written_products = set()  # To keep track of written products
    with open(products_output_file, 'w', newline='') as products_csv:
        products_writer = csv.writer(products_csv)
        products_writer.writerow(['ASIN', 'title', 'group', 'sales_rank', 'category_id', 'similar_ASINs'])

        for entry in data.values():
            asin = entry['ASIN']
            title = entry['title']
            group = entry['group']
            sales_rank = entry['salesrank']
            for category in entry['categories']:
                categories = category.strip('|').split('|')
                for category_str in categories:
                    category_id = category_str.split('[')[-1].rstrip(']')
                    product_key = (asin, category_id)  # Unique key for a product entry
                    if product_key not in written_products:
                      written_products.add(product_key)
                      for similar_asin in entry['similar'][1:]:  # Exclude the first item
                          products_writer.writerow([asin, title, group, sales_rank, category_id, similar_asin])
                      