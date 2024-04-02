from json_to_csv import json_to_csv
from txt_to_json import txt_to_json

def main():
    txt_path = "../Data/amazon-meta.txt"
    json_path = "../Data/data.json"
    txt_to_json(input_file=txt_path, output_file=json_path)
    products_path = "../Outputs/products.csv"
    categories_path = "../Outputs/categories.csv"
    json_to_csv(input_file=json_path, products_output_file=products_path, categories_output_file=categories_path)

if __name__ == '__main__':
    main()