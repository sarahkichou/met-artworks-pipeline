import json
import os
from collections import Counter
from extract import fetch_object_ids, fetch_object_details
from transform import transform_objects

def main():
    ids_file = "object_ids.json"

    if os.path.exists(ids_file):
        with open(ids_file, "r") as file:
            objects = json.load(file)
    else:
        objects = fetch_object_ids()
        with open(ids_file, "w") as file:
            json.dump(objects, file)
    
    details_file = "object_details.json"

    if os.path.exists(details_file):
        with open(details_file, "r") as file:
            all_details = json.load(file)

        print("Loaded existing extracted records:", len(all_details))

    else:
        all_details = []
        all_failed_ids = {}

        # Test slice configuration
        start = 300000
        end = 320000
        chunk_size = 100

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

        print("Successful records:", len(all_details))
        print("Failed records:", len(all_failed_ids))
        print("403 failures:", list(all_failed_ids.values()).count(403))

        print(Counter(all_failed_ids.values()))

        with open(details_file, "w") as file:
            json.dump(all_details, file)
    
    met_df = transform_objects(all_details)
    print(met_df.shape)

if __name__ == "__main__":
    main()