from datetime import date, timedelta
from ingestion.weather import run_pipeline


def backfill(start_date, end_date):
    current_date = start_date

    while current_date <= end_date:
        print(f"Processing {current_date}")
        run_pipeline(current_date.isoformat())
        current_date += timedelta(days=1)


if __name__ == "__main__":
    # Assessment backfill: last 30 calendar days.
    end_date = date(2026, 9, 8)
    start_date = end_date - timedelta(days=29)

    backfill(start_date, end_date)