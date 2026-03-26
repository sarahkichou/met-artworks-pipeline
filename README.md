# Met Museum Artworks Data Pipeline

## Overview

This project builds an end-to-end data pipeline to extract, transform, and load artwork data from the Metropolitan Museum of Art API into a PostgreSQL database.

The goal is to simulate a real-world data engineering workflow, including handling incomplete data, API limitations, and designing a clean relational schema.

---

## Dataset

- Source: Met Museum API  
- Total available object IDs: ~500,000  
- Sample requested: ~20,000 artworks  
- Successfully extracted: ~16,000 artworks (after API failures)

During development, API requests were initially tested on small subsets of IDs before scaling extraction.

---

## Pipeline Architecture

### 1. Extract

- Object IDs are retrieved from the API and stored locally
- Artwork details are fetched in batches using a chunking approach
- Random sampling is used to create a more representative subset of data
- Data is cached in `object_details.json` to avoid repeated API calls

#### API Failures Handling

- Frequent HTTP 403 responses were encountered  
- Failed requests are logged and skipped  
- Chunking and batching strategies were adjusted based on experimentation  

---

### 2. Transform

Key transformations applied:

- Converted empty strings and `"NaN"` values to `NULL`
- Standardised text fields (trimmed whitespace)
- Normalised artist data into a separate table
- Created a surrogate `artist_id`
- Linked artworks to artists via foreign key
- Fixed inconsistent date ranges (e.g. BCE dates where begin > end)
- Preserved distinctions between:
  - `NULL` → missing artist information  
  - `"Unknown"` → explicitly labelled unknown artist  
  - `"Anonymous"` → intentionally anonymous attribution  

Artists were deduplicated based on cleaned `artist_display_name`, though this does not fully resolve spelling or naming variations.

---

### 3. Load

- Data is loaded into PostgreSQL
- Tables:
  - `artworks`
  - `artists`
- Primary and foreign key constraints enforced
- Idempotent loading implemented using `ON CONFLICT DO NOTHING`

---

## Extraction Experiments

During development, different extraction strategies were tested to balance performance and API reliability.

The Met API frequently returned HTTP 403 responses when requesting large batches or sending requests too quickly.

| Slice | Limit | Sleep | Success | Failed | Failure Code |
|------|------|------|------|------|------|
| 0–500 | 500 | 0.05 | 79 | 421 | 403 |
| 10000–10500 | 500 | 0.05 | 275 | 225 | 403 |
| 300000–300500 | 500 | 0.05 | 290 | 210 | 403 |
| 300000–300500 | 500 | 0.00 | 95 | 405 | 403 |
| 300000–300500 | 500 | 0.10 | 80 | 420 | 403 |
| 300000–300100 | 100 | 0.00 | 100 | 0 | N/A |
| 300100–300200 | 100 | 0.00 | 99 | 1 | 403 |
| 300200–300300 | 100 | 0.00 | 82 | 18 | 403 |
| 300300–300400 | 100 | 0.00 | 96 | 4 | 403 |
| 300400–300500 | 100 | 0.00 | 100 | 0 | N/A |

These experiments informed the final batching strategy used in the pipeline.

---

## Data Challenges & Decisions

### Missing Artist Data

A large proportion of artworks do not have attributed artists. This reflects the nature of historical and archaeological collections rather than data quality issues.

Different cases were handled separately:

- `NULL` → no artist information provided  
- `"Unknown"` → explicitly labelled unknown  
- `"Anonymous"` → intentionally anonymous  

These were preserved rather than merged to maintain data integrity.

---

### Country Field

~80% of records had missing country values.

Due to the high level of sparsity, this field was not prioritised for further use.

---

## Schema Design

The dataset was partially normalised:

- `artists` table created to reduce duplication and model a real entity
- `artworks` table references artists via foreign key
- Other fields (e.g. department, classification) were kept denormalised to avoid overengineering

---

## Key Learnings

- Handling incomplete and inconsistent real-world data  
- Designing a practical relational schema  
- Balancing normalisation vs simplicity  
- Building resilient pipelines with API limitations