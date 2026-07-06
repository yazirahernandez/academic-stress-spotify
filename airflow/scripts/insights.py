import logging

logger = logging.getLogger(__name__)


def generate_insights(df):
    stress = df[df["week_type"] == "high-stress"]
    normal = df[df["week_type"] == "normal"]

    logger.info(
        "[INSIGHTS] Segmenting clean data: %d stress-period rows, %d normal-period rows",
        len(stress), len(normal),
    )

    insights = {
        "avg_tempo_stress": float(stress["tempo"].mean()),
        "avg_tempo_normal": float(normal["tempo"].mean()),
        "avg_energy_stress": float(stress["energy"].mean()),
        "avg_energy_normal": float(normal["energy"].mean()),
    }

    insights["stress_behavior"] = (
        "Higher stimulation music during stress periods"
        if insights["avg_energy_stress"] > insights["avg_energy_normal"]
        else "No significant stress-driven change"
    )

    logger.info(
        "[INSIGHTS] avg_tempo_stress=%.2f avg_tempo_normal=%.2f "
        "avg_energy_stress=%.2f avg_energy_normal=%.2f -> %s",
        insights["avg_tempo_stress"], insights["avg_tempo_normal"],
        insights["avg_energy_stress"], insights["avg_energy_normal"],
        insights["stress_behavior"],
    )

    # Which specific deadline (from academic_calendar.csv) coincides with the
    # most intense listening, so the dashboard can point at a concrete week
    # instead of just saying "stress periods" in the abstract.
    deadline_energy = (
        stress.dropna(subset=["project_deadline"])
        .groupby("project_deadline")["energy"]
        .mean()
        .sort_values(ascending=False)
    )

    if not deadline_energy.empty:
        insights["peak_stress_deadline"] = deadline_energy.index[0]
        insights["peak_stress_deadline_energy"] = float(deadline_energy.iloc[0])
        logger.info(
            "[INSIGHTS] Peak stress deadline: '%s' (avg energy %.2f)",
            insights["peak_stress_deadline"], insights["peak_stress_deadline_energy"],
        )
    else:
        insights["peak_stress_deadline"] = None
        insights["peak_stress_deadline_energy"] = None
        logger.info("[INSIGHTS] No deadline data available to rank")

    return insights
