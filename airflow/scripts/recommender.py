def recommend(insights):

    if insights["avg_energy_stress"] > insights["avg_energy_normal"]:
        return {
            "mood": "stress",
            "playlist_type": "calming regulation",
            "recommendations": [
                "Lo-fi beats",
                "Ambient study music",
                "Soft piano focus"
            ]
        }

    return {
        "mood": "balanced",
        "playlist_type": "productivity focus",
        "recommendations": [
            "Deep work electronic",
            "Instrumental techno",
            "Focus coding playlists"
        ]
    }
