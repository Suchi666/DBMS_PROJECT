from json_to_csv import json_to_csv


def main():
    json_to_csv('../Data/data.json', '../Outputs/products.csv', '../Outputs/categories.csv')


if __name__ == '__main__':
    main()