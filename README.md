# Data Engineering Assessment

Build **one small, working, end-to-end data pipeline** and walk us through it in a notebook.
Scope is deliberately small: we want to see a pipeline that actually runs, is safe to re-run,
and that you can explain. Nothing here needs to be "production scale".

## The task

Daily weather for the cities in `config/cities.yml`, from the free
[Open-Meteo archive API](https://open-meteo.com/en/docs/historical-weather-api) (no key),
for the last 30 days.

```
Open-Meteo API  ──extract──▶  raw.weather_daily (Postgres)
                              │
                              └──dbt──▶ staging.stg_weather ──▶ marts.fct_city_daily
                                                          (tests + docs)
                 Airflow DAG:  extract → load → dbt run → dbt test   (daily, backfillable)
                 Notebook:     runs every stage, shows the results, explains the choices
```

### 1. Extract & load (Python)

- One run loads **one logical date** (and a helper can load a date range for backfill).
- Re-running the same date must **not** duplicate rows. Choose a mechanism
  (delete + insert, upsert, partition overwrite) and be ready to defend it.
- Keep the API fields unmodified in the raw table; transformation belongs in dbt.
- Timeouts and retries on the HTTP call.

### 2. Transform (dbt)

- Declare `raw.weather_daily` as a **source**.
- A staging model that types and cleans the raw rows.
- One mart, for example daily aggregates per city (`marts.fct_city_daily`).
- Schema tests that would catch a real regression (keys, ranges, nulls), and descriptions
  on models and columns.

### 3. Orchestrate (Airflow)

- One DAG: `extract → load → dbt run → dbt test`, scheduled daily.
- Use the **logical date** (`{{ ds }}` / `data_interval_start`) so `airflow dags backfill`
  works. No hard-coded "today".
- Tasks are idempotent on rerun; sensible retries and timeouts.

### 4. Walk through (notebook)

`notebooks/walkthrough.ipynb` is how we read your solution. It must:

1. Run each stage in order using the **same code the DAG uses** (import your functions or
   trigger the DAG; do not re-implement the logic in the notebook).
2. After each stage, show evidence: row counts, a few sample rows, dbt run/test output.
3. Prove re-run safety: run the load for the same date twice and show counts are unchanged.
4. Query the mart and show a result a business user would recognise.
5. Explain, in short markdown cells, what each stage does and **why** you built it that way.

Commit the notebook **with its outputs**. A notebook without outputs scores as not run.

### 5. Notes

Fill in `NOTES.md`: time spent, known gaps, and exactly what you used AI tools for.

### Reproducibility

We review by cloning your repository on a clean machine and running:

```bash
cp .env.example .env
make up          # everything comes up
make reproduce   # executes notebooks/walkthrough.ipynb headlessly
```

`make reproduce` must succeed without manual steps. Run it yourself before submitting.

## Rules on AI assistance

You may use AI tools the way you would at work: to look things up, unblock yourself, review
your own code. You may not have them build the solution for you. Be specific in `NOTES.md`.
The follow-up interview goes through your code and notebook in detail.

## How this is assessed

Six dimensions, 0–5 each: extract & load, dbt modelling, orchestration, data quality,
notebook walkthrough, code quality. A pipeline that visibly runs end to end matters more
than any single feature. Commit history is visible to reviewers, so commit in steps.

## Getting started

```bash
cp .env.example .env
make up          # postgres, airflow (standalone), jupyter
make airflow-ui  # http://localhost:8080  (admin / admin)
make notebook    # http://localhost:8888  (JupyterLab, no token)
make dbt         # dbt run inside the airflow container
make reproduce   # execute the notebook headlessly (what reviewers run)
make down
```

The scaffold starts the services but contains **no pipeline logic**. Everything under
`dags/`, `ingestion/`, `dbt/models/` and `notebooks/` is yours to write. Restructure as you
like, as long as `make up` and `make reproduce` still work.

## Submitting

Push to the default branch, open the portal, answer two short questions, and press Submit.
Submission records the current commit and makes the repository read-only for you. Submit once.
