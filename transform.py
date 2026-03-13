import pandas as pd

def transform_objects(all_objects):
    met_df = pd.DataFrame(all_objects)
    met_df = met_df[["objectID", "isHighlight", "department", "objectName", "title", "culture", "period", "artistDisplayName", "artistNationality", "artistGender", "objectDate", "objectBeginDate", "objectEndDate", "medium", "dimensions", "country", "classification", "objectURL"]]
    
    return met_df