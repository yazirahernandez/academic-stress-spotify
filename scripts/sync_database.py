import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: Connect to PostgreSQL and sync data
def sync_academic_calendar():
    df = pd.read_csv('data/academic_calendar.csv')
    # Insert into database
    pass

def sync_students():
    df = pd.read_csv('data/students.csv')
    # Insert into database
    pass

def sync_track_selections():
    df = pd.read_csv('data/track_selections.csv')
    # Insert into database
    pass

if __name__ == "__main__":
    print("Syncing data to database...")
    sync_academic_calendar()
    sync_students()
    sync_track_selections()
    print("✅ Sync complete!")
