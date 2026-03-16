import json
import os
from collections import Counter
from extract import fetch_object_ids, fetch_object_details
from transform import transform_objects
from load import load_artworks

def load_json_file(path):
    with open(path, "r") as file:
        return json.load(file)
    
def save_json_file(path, data):
    with open(path, "w") as file:
        json.dump(data, file)
    
def get_object_ids(ids_file):
    if os.path.exists(ids_file):
        return load_json_file(ids_file)

    objects = fetch_object_ids()
    save_json_file(ids_file, objects) 
    return objects


def extract_details(objects, start, end, chunk_size):
    all_details = []
    all_failed_ids = {}

    object_ids = objects["objectIDs"][start:end]
    batch_num = 1

    for chunk_start in range(0, len(object_ids), chunk_size):
        chunk_ids = object_ids[chunk_start:chunk_start + chunk_size]

        print(f"Processing batch {batch_num}")
        batch_num += 1

        chunk_objects = {"objectIDs": chunk_ids}
        details, failed_ids = fetch_object_details(chunk_objects, limit=len(chunk_ids))

        all_details.extend(details)
        all_failed_ids.update(failed_ids)

    return all_details, all_failed_ids

def get_object_details(details_file, objects, start, end, chunk_size):
    if os.path.exists(details_file):
        all_details = load_json_file(details_file)

        print("Loaded existing extracted records:", len(all_details))

        return all_details

    all_details, all_failed_ids = extract_details(objects, start, end, chunk_size)

    print("Successful records:", len(all_details))
    print("Failed records:", len(all_failed_ids))
    print(Counter(all_failed_ids.values()))

    save_json_file(details_file, all_details)
    return all_details

def main():
    ids_file = "data/object_ids.json"
    details_file = "data/object_details.json"

    start = 300000
    end = 320000
    chunk_size = 100

    objects = get_object_ids(ids_file)
    all_details = get_object_details(details_file, objects, start, end, chunk_size)

    met_df = transform_objects(all_details)
    print(met_df.shape)
    print((met_df == "").sum())

    load_artworks(met_df)

if __name__ == "__main__":
    main()