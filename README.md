500382 IDs in total

During development, API requests were tested on small subsets of IDs before scaling extraction.

The extraction function is designed to process the full object ID list (~500k records).
For development purposes the pipeline is run on a limited subset.

Some object IDs returned HTTP 403 responses during extraction.
The pipeline records failed IDs and continues processing.

During transformation, empty strings returned by the Met API were converted to NULL values to ensure correct handling of missing data in PostgreSQL.


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