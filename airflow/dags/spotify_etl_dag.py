from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import pandas as pd
import numpy as np
import json

def extract():
    df = pd.DataFrame({
        "track_id": range(500),
        "tempo": np.random.normal(120, 20, 500),
        "energy": np.random.uniform(0.2, 1.0, 500),
        "week_type": np.random.choice(["normal", "stress"], 500, p=[0.6, 0.4])
    })
    df.to_json("/opt/airflow/data/raw.json")
    print("EXTRACT OK")

def transform():
    df = pd.read_json("/opt/airflow/data/raw.json")
    df = df[(df["tempo"] > 60) & (df["tempo"] < 200)]
    df.to_json("/opt/airflow/data/clean.json")
    print("TRANSFORM OK")

def load():
    df = pd.read_json("/opt/airflow/data/clean.json")

    insights = {
        "avg_tempo": float(df["tempo"].mean()),
        "avg_energy": float(df["energy"].mean())
    }

    with open("/opt/airflow/data/insights.json", "w") as f:
        json.dump(insights, f)

    print("LOAD OK")

with DAG(
    dag_id="spotify_stress_pipeline",
    start_date=datetime(2024,1,1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t3 = PythonOperator(task_id="load", python_callable=load)

    t1 >> t2 >> t3
