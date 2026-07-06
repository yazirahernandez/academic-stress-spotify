import json
import logging
import os
import sys
from datetime import datetime

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

# ---------------------------------------------------------------------------
# Make the modular ETL scripts (airflow/scripts/*.py) importable from the DAG
# file (airflow/dags/spotify_etl_dag.py). Adjust these paths if your
# docker-compose volumes mount the scripts folder somewhere else.
# ---------------------------------------------------------------------------
_LOCAL_SCRIPTS_PATH = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.append(os.path.abspath(_LOCAL_SCRIPTS_PATH))
sys.path.append("/opt/airflow/scripts")  # container layout set up in docker-compose.yml

from extract import extract_dummy_spotify, extract_academic_calendar  # noqa: E402
from transform import transform  # noqa: E402
from insights import generate_insights  # noqa: E402
from recommender import recommend  # noqa: E402

logger = logging.getLogger(__name__)

DATA_DIR = "/opt/airflow/data"


def extract_task():
    spotify_df = extract_dummy_spotify()
    calendar_df = extract_academic_calendar(csv_path=f"{DATA_DIR}/academic_calendar.csv")

    spotify_df.to_json(f"{DATA_DIR}/raw_spotify.json", date_format="iso")
    calendar_df.to_json(f"{DATA_DIR}/raw_calendar.json", date_format="iso")

    logger.info(
        "[EXTRACT] Stage complete: %d Spotify rows + %d calendar weeks written to disk",
        len(spotify_df), len(calendar_df),
    )


def transform_task():
    spotify_df = pd.read_json(f"{DATA_DIR}/raw_spotify.json", convert_dates=["play_date"])
    calendar_df = pd.read_json(f"{DATA_DIR}/raw_calendar.json", convert_dates=["start_date", "end_date"])

    clean_df = transform(spotify_df, calendar_df)
    clean_df.to_json(f"{DATA_DIR}/clean.json", date_format="iso")

    logger.info("[TRANSFORM] Stage complete: %d clean rows written to clean.json", len(clean_df))


def insights_task():
    clean_df = pd.read_json(f"{DATA_DIR}/clean.json", convert_dates=["play_date"])
    metrics = generate_insights(clean_df)

    with open(f"{DATA_DIR}/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    logger.info("[INSIGHTS] Stage complete: metrics.json written with keys %s", list(metrics.keys()))


def load_task():
    with open(f"{DATA_DIR}/metrics.json") as f:
        metrics = json.load(f)

    rec = recommend(metrics)
    final_output = {**metrics, **rec}

    with open(f"{DATA_DIR}/insights.json", "w") as f:
        json.dump(final_output, f, indent=2)

    logger.info(
        "[LOAD] Stage complete: final insights.json written with keys %s",
        list(final_output.keys()),
    )


with DAG(
    dag_id="spotify_stress_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id="extract", python_callable=extract_task)
    t2 = PythonOperator(task_id="transform", python_callable=transform_task)
    t3 = PythonOperator(task_id="generate_insights", python_callable=insights_task)
    t4 = PythonOperator(task_id="load", python_callable=load_task)

    t1 >> t2 >> t3 >> t4
