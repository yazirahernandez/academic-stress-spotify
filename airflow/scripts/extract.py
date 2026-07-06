import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# The semester window covered by data/academic_calendar.csv. Both dummy
# sources reference this so they describe the same time period, without one
# source needing to read the other's output.
SEMESTER_START = pd.Timestamp("2024-01-08")
SEMESTER_END = pd.Timestamp("2024-04-29")


def extract_dummy_spotify(n=600, seed=42):
    """Source 1: simulated Spotify-like listening data (dummy data, OK'd by
    the professor). One row per track play, with tempo, energy, and the
    calendar date it was played on, spread across the semester.
    """
    np.random.seed(seed)
    total_days = (SEMESTER_END - SEMESTER_START).days
    day_offsets = np.random.randint(0, total_days + 1, n)
    play_dates = SEMESTER_START + pd.to_timedelta(day_offsets, unit="D")

    df = pd.DataFrame({
        "track_id": range(n),
        "tempo": np.random.normal(120, 22, n),
        "energy": np.random.uniform(0.2, 1.0, n),
        "play_date": play_dates,
    })
    logger.info(
        "[EXTRACT] Spotify source: %d rows generated (play_date range %s to %s)",
        len(df), play_dates.min().date(), play_dates.max().date(),
    )
    return df


def extract_academic_calendar(csv_path="data/academic_calendar.csv"):
    """Source 2: real academic calendar (week_number, start_date, end_date,
    week_type, project_deadline) loaded from CSV.
    """
    df = pd.read_csv(csv_path, parse_dates=["start_date", "end_date"])
    stress_weeks = int((df["week_type"] == "high-stress").sum())
    logger.info(
        "[EXTRACT] Academic calendar source: %d weeks loaded from %s (%d high-stress, %d normal)",
        len(df), csv_path, stress_weeks, len(df) - stress_weeks,
    )
    return df


# Backward-compatible alias in case anything still imports the old name.
extract_dummy = extract_dummy_spotify
