import psycopg2

create_artists_table = """
CREATE TABLE IF NOT EXISTS artists (
    artist_id int PRIMARY KEY,
    artist_display_name text,
    artist_nationality text,
    artist_gender text
)
""" 

insert_artists = """
INSERT INTO artists (
    artist_id,
    artist_display_name,
    artist_nationality,
    artist_gender
)

VALUES (%s, %s, %s, %s)
ON CONFLICT (artist_id) DO NOTHING
"""

create_artworks_table = """
CREATE TABLE IF NOT EXISTS artworks (
    object_id int PRIMARY KEY,
    artist_id int,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    is_highlight boolean, 
    department text,
    object_name text,
    title text,
    culture text,
    period text,
    object_date text,
    object_begin_date int,
    object_end_date int,
    medium text,
    dimensions text,
    country text,
    classification text,
    object_url text
    )
""" 

insert_artworks = """
INSERT INTO artworks (
    object_id,
    artist_id,
    is_highlight, 
    department,
    object_name,
    title,
    culture,
    period,
    object_date,
    object_begin_date,
    object_end_date,
    medium,
    dimensions,
    country,
    classification,
    object_url
    )

VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (object_id) DO NOTHING
"""

def load_artists(artists_df):
    conn = psycopg2.connect(
        database="met_db",
        user="sarahkichou",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(create_artists_table)
    row_tuples = list(artists_df.itertuples(index=False, name=None))
    cursor.executemany(insert_artists, row_tuples)
    conn.commit()
    
    cursor.close()
    conn.close()

def load_artworks(artworks_df):
    conn = psycopg2.connect(
        database="met_db",
        user="sarahkichou",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(create_artworks_table)
    row_tuples = list(artworks_df.itertuples(index=False, name=None))
    cursor.executemany(insert_artworks, row_tuples)
    conn.commit()
    
    cursor.close()
    conn.close()