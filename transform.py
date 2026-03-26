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
    
    met_df.columns = [
        "object_id", 
        "is_highlight", 
        "department", 
        "object_name", 
        "title", 
        "culture", 
        "period", 
        "artist_display_name", 
        "artist_nationality", 
        "artist_gender", 
        "object_date", 
        "object_begin_date", 
        "object_end_date", 
        "medium", 
        "dimensions", 
        "country", 
        "classification", 
        "object_url"]

    # Standardise text columns
    columns = [
        "department",
        "object_name",
        "title",
        "culture",
        "period",
        "artist_display_name",
        "artist_nationality",
        "artist_gender",
        "object_date",
        "medium",
        "dimensions",
        "country",
        "classification",
        "object_url"]
    
    for column in columns:
        met_df[column] = met_df[column].str.strip()

    # Replace empty strings and "NaN" placeholders with None for proper NULL handling in PostgreSQL
    met_df.replace(["", "NaN"], None, inplace=True)

    # Create a unique artist table for normalisation
    artists_df = met_df[
        ["artist_display_name", "artist_nationality", "artist_gender"]
        ].drop_duplicates()
    
    # Reset index after deduplication
    artists_df = artists_df.reset_index(drop=True)

    # Assign a surrogate key to each unique artist
    artists_df["artist_id"] = range(1, len(artists_df) + 1)
    
    # Join artist_id back to met_df to create a foreign key relationship
    met_df = met_df.merge(
        artists_df, 
        on=["artist_display_name", "artist_nationality", "artist_gender"],
        how="left"
    )
    
    # Remove denormalised artist columns now that artist_id is linked
    artworks_df = met_df.drop(
        labels=["artist_display_name", 
                "artist_nationality", 
                "artist_gender"],
        axis=1,
    )
    
    artists_df = artists_df[[
        "artist_id", 
        "artist_display_name", 
        "artist_nationality", 
        "artist_gender"
    ]]

    artworks_df = artworks_df[[
        "object_id",
        "artist_id",
        "is_highlight",
        "department",
        "object_name",
        "title",
        "classification",
        "culture",
        "period",
        "object_date",
        "object_begin_date",
        "object_end_date",
        "medium",
        "dimensions",
        "country",
        "object_url"
    ]]

    # Fix rows where object_begin_date is after object_end_date (BCE dates reversed)
    condition = artworks_df["object_begin_date"] > artworks_df["object_end_date"]

    if condition.any():
        print(f"Fixing {condition.sum()} rows where begin_date > end_date")

        artworks_df.loc[condition, ["object_begin_date", "object_end_date"]] = (
            artworks_df.loc[condition, ["object_end_date", "object_begin_date"]].values
        )

    if artworks_df["object_id"].isnull().any():
        raise ValueError("object_id contains NULL values")
    
    if not artworks_df["object_id"].is_unique:
        raise ValueError("Duplicate object_id detected")
    
    if not artists_df["artist_id"].is_unique:
        raise ValueError("Duplicate artist_id detected")

    return artworks_df, artists_df