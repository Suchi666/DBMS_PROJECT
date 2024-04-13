import re
import json

def txt_to_list(input_file):
    items_list = {}
    i=1
    items_list[1]=[]
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                i+=1
                items_list[i] = []
            else:
                items_list[i].append(line)
    
    return items_list

def parse_items_list(items_list):
    data = {}
    count = -1
    for _, lines in items_list.items():
        current_entry = {}
        reviews_info = None
        categories_count = 0
        review = 0
        categories_lines = []
        count = count + 1
        if count == 8000: # considers only 8,000 products
            break
        for line in lines:
            if line.startswith("Id:"):
                current_entry["Id"] = line.split()[1]
            elif "discontinued product" in line:
                current_entry = None
                break  # Skip this item if it's discontinued
            elif current_entry:
                if ':' in line and review == 0:
                    key, value = re.split(r'\s*:\s*', line, maxsplit=1)
                    if key == "ASIN":
                        current_entry[key] = value.strip()
                    elif key in ["title", "group", "salesrank"]:
                        current_entry[key] = value.strip()
                        '''
                        if key == "group" and current_entry[key] != "Book":
                            current_entry = None
                            break 
                        '''
                    elif key == "similar":
                        current_entry[key] = value.strip().split()[1:]
                    elif key == "categories":
                        categories_count = int(value.strip())
                    elif key == "reviews":
                        reviews_info = value.strip().split()
                        current_entry[key] = {
                            "total": reviews_info[1],
                            "downloaded": reviews_info[3],
                            "rating": reviews_info[6],
                            "individual_reviews": []  # Initialize individual_reviews here
                        }
                        categories_count = 0
                        review = 1
                else:
                    # Handle multiline reviews
                    if categories_count > 0:
                        categories_lines.append(line)
                        categories_count -= 1
                    elif review == 1:
                        reviews_info = line.strip().split()
                        if len(reviews_info) >= 9:  # Ensure that there are enough elements in the list
                            current_entry["reviews"]["individual_reviews"].append({
                                "date": reviews_info[0],
                                "customer": reviews_info[2],
                                "rating": reviews_info[4],
                                "votes": reviews_info[6],
                                "helpful": reviews_info[8]
                            })
        if current_entry:
            current_entry["categories"] = [c.strip() for c in categories_lines]
            data[str(current_entry["Id"])] = current_entry

    return data

def write_list_to_file(items_list, output_file):
    with open(output_file, 'w') as file:
        for key, value in items_list.items():
            file.write(f"{key}: {value}\n")

def txt_to_json(input_file, output_file):
    items_list = txt_to_list(input_file=input_file)
    print("step 1.1 done")
    write_list_to_file(items_list, "../Outputs/items_list.txt")
    print("step 1.2 done")
    data = parse_items_list(items_list=items_list)
    print("step 1.3 done")
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)
        print("step 1.4 done")


