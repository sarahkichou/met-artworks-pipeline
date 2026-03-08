import json
import os
from extract import fetch_object_ids, fetch_object_details

def main():
    ids_file = "object_ids.json"

    if os.path.exists(ids_file):
         with open(ids_file, "r") as file:
             objects = json.load(file)
    else:
        objects = fetch_object_ids()
        with open(ids_file, "w") as file:
            json.dump(objects, file)

    test_objects = {"objectIDs": objects["objectIDs"][300400:300500]}
    details, failed_ids = fetch_object_details(test_objects, limit=100)   

    print("Successful records:", len(details))
    print("Failed records:", len(failed_ids))

    print(list(failed_ids.values()).count(403))

if __name__ == "__main__":
    main()