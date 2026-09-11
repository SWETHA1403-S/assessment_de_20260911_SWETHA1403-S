# NOTES

## Time spent

Approximately 5-6 hours were spent building, testing, documenting, and verifying the pipeline.

## Known gaps

- The pipeline is intentionally small and uses three cities.
- The pipeline uses the Open-Meteo historical weather API.
- The current solution focuses on daily weather data and does not include production-scale monitoring or alerting.
- Airflow and dbt are configured for the scope of this assessment.

## AI tools used

I used AI tools as development assistance, not as a replacement for understanding or testing the solution.

| Where | What the AI tool was used for | What I changed / verified afterwards |
| --- | --- | --- |
| Python ingestion | Asked for help understanding API requests, retries, and error handling | Reviewed and adapted the code to fit the project |
| PostgreSQL | Asked about idempotent loading and primary keys | Implemented and verified the delete-and-insert approach |
| dbt | Asked about dbt sources, staging models, tests, and PostgreSQL configuration | Implemented the models and tests and verified dbt execution |
| Airflow | Asked about DAG scheduling, logical dates, retries, and task dependencies | Implemented and tested the DAG |
| Docker | Asked for help understanding Docker Compose/service configuration | Adapted the configuration and verified the services |
| Notebook | Asked for help troubleshooting notebook execution and displaying verification results | Ran the notebook and verified the outputs |

## Verification

The pipeline was tested using Docker Compose.

The walkthrough notebook was executed from top to bottom and committed with its outputs.

The ingestion process was also re-run for the same logical date to verify that the row count remained unchanged and duplicate city/date records were not created.
