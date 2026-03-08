import time
import requests
from tqdm import tqdm

# Store API URL in variable
objects_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

# Function to fetch objects data from API and store as JSON
def fetch_object_ids():
    response = requests.get(objects_url, timeout=10)

    return response.json()

# Function looping through object IDs to retrieve object details from API
def fetch_object_details(objects, limit=100):
    all_objects = []
    failed_ids = {}
    
    for object_id in tqdm(objects["objectIDs"][:limit]):
        try:
            object_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
            response = requests.get(object_url, timeout=10)

            if response.status_code == 200:
                all_objects.append(response.json())
            else:
                failed_ids[object_id] = response.status_code
                
        except Exception:
            print("Error fetching:", object_id)
            failed_ids[object_id] = "exception"
        
    return all_objects, failed_ids
