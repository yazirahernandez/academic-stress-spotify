def generate_insights(df):

    stress = df[df["week_type"] == "stress"]
    normal = df[df["week_type"] == "normal"]

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

    return insights
