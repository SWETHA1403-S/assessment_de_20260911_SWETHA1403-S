.PHONY: up down logs airflow-ui notebook dbt dbt-test psql reproduce

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f airflow

airflow-ui:
	@echo "Airflow:    http://localhost:8080  (admin / admin)"

notebook:
	@echo "JupyterLab: http://localhost:8888  (open notebooks/walkthrough.ipynb)"

dbt:
	docker compose exec airflow bash -c "cd /opt/airflow/dbt && dbt run"

dbt-test:
	docker compose exec airflow bash -c "cd /opt/airflow/dbt && dbt test"

psql:
	docker compose exec postgres psql -U $${POSTGRES_USER:-de} -d $${POSTGRES_DB:-warehouse}

# Executes the walkthrough top to bottom with a fresh kernel and writes the result next to it.
# Reviewers run this on a clean checkout and diff it against the committed notebook.
reproduce:
	docker compose exec jupyter jupyter nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=1800 \
		--output walkthrough.reproduced.ipynb /opt/airflow/notebooks/walkthrough.ipynb
	@echo "Wrote notebooks/walkthrough.reproduced.ipynb"
