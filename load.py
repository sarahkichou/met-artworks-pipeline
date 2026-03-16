import psycopg2

create_table = """
CREATE TABLE IF NOT EXISTS artworks (
    objectID int PRIMARY KEY,
    isHighlight boolean, 
    department text,
    objectName text,
    title text,
    culture text,
    period text,
    artistDisplayName text,
    artistNationality text,
    artistGender text,
    objectDate text,
    objectBeginDate int,
    objectEndDate int,
    medium text,
    dimensions text,
    country text,
    classification text,
    objectURL text
    )
""" 

insert_artworks = """
INSERT INTO artworks (objectID,
    isHighlight, 
    department,
    objectName,
    title,
    culture,
    period,
    artistDisplayName,
    artistNationality,
    artistGender,
    objectDate,
    objectBeginDate,
    objectEndDate,
    medium,
    dimensions,
    country,
    classification,
    objectURL)

VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (objectID) DO NOTHING
"""

def load_artworks(met_df):
    conn = psycopg2.connect(
        database="met_db",
        user="sarahkichou",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

    row_tuples = list(met_df.itertuples(index=False, name=None))

    cursor.execute(create_table)
    cursor.executemany(insert_artworks, row_tuples)
    conn.commit()
    
    cursor.close()
    conn.close()

