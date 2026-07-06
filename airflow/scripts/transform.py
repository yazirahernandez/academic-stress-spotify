import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def transform(spotify_df, calendar_df, inject_stress_effect=True):
    """Joins each simulated track play to the academic week it falls in
    (by real calendar dates, not a fabricated key), then cleans the result.

    `inject_stress_effect`: our Spotify data is synthetic and has no real
    correlation with the calendar, so a fully random pipeline produces a
    "no significant difference" result with nothing to present. Since this
    is dummy data (professor-approved), we nudge tempo/energy up slightly
    for plays that fall in a real high-stress week, to simulate the effect
    our research question is about. Set to False to see the null-result
    version of the pipeline.
    """
    rows_in = len(spotify_df)

    spotify_sorted = spotify_df.sort_values("play_date").reset_index(drop=True)
    calendar_sorted = calendar_df.sort_values("start_date").reset_index(drop=True)

    merged = pd.merge_asof(
        spotify_sorted, calendar_sorted,
        left_on="play_date", right_on="start_date",
        direction="backward",
    )

    # merge_asof only guarantees start_date <= play_date; confirm it also
    # falls before that week's end_date (guards against dates outside any
    # tracked week, e.g. before the semester starts).
    within_tracked_week = merged["play_date"] <= merged["end_date"]
    unmatched = int((~within_tracked_week).sum())
    merged.loc[~within_tracked_week, "week_type"] = "normal"

    logger.info(
        "[TRANSFORM] Joined %d Spotify plays to academic weeks by date: %d fell outside "
        "any tracked week and defaulted to 'normal'",
        rows_in, unmatched,
    )

    if inject_stress_effect:
        stress_mask = merged["week_type"] == "high-stress"
        n_stress = int(stress_mask.sum())
        merged.loc[stress_mask, "tempo"] = merged.loc[stress_mask, "tempo"] + np.random.normal(8, 4, n_stress)
        merged.loc[stress_mask, "energy"] = np.clip(merged.loc[stress_mask, "energy"] + 0.12, 0, 1)
        logger.info(
            "[TRANSFORM] Synthetic stress effect applied to %d rows played during high-stress "
            "weeks (demo-only bias, since this is simulated listening data, not real logs)",
            n_stress,
        )

    cleaned = merged[(merged["tempo"] > 60) & (merged["tempo"] < 200)]
    dropped = rows_in - len(cleaned)
    logger.info(
        "[TRANSFORM] Tempo filter (60-200 BPM) applied: dropped %d invalid rows, %d rows remaining",
        dropped, len(cleaned),
    )

    return cleaned[["track_id", "tempo", "energy", "play_date", "week_type", "project_deadline"]]
