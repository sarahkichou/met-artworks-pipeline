import pandas as pd

def transform_objects(all_objects):
    met_df = pd.DataFrame(all_objects)
    met_df = met_df[
        ["objectID", 
         "isHighlight", 
         "department", 
         "objectName", 
         "title", 
         "culture", 
         "period", 
         "artistDisplayName", 
         "artistNationality", 
         "artistGender", 
         "objectDate", 
         "objectBeginDate", 
         "objectEndDate", 
         "medium", 
         "dimensions", 
         "country", 
         "classification", 
         "objectURL"]]
    
    # Convert empty strings from the API to None so they become NULL in PostgreSQL
    met_df.replace("", None, inplace=True)

    if met_df["objectID"].isnull().any():
        raise ValueError("objectID contains NULL values")
    
    if not met_df["objectID"].is_unique:
        raise ValueError("Duplicate objectIDs detected")
    
    return met_df

