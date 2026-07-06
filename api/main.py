from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

app = FastAPI()


def clamp_pct(value: float, low: float, high: float) -> float:
    if high == low:
        return 0.0
    pct = (value - low) / (high - low) * 100
    return max(0, min(100, pct))


@app.get("/")
def root():
    return {"status": "running"}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    try:
        with open("data/insights.json") as f:
            insights = json.load(f)
    except Exception:
        insights = {}

    # These are the keys the pipeline's load stage actually writes now
    # (generate_insights() + recommend() merged together in load_task()).
    avg_tempo_stress = float(insights.get("avg_tempo_stress", 0) or 0)
    avg_tempo_normal = float(insights.get("avg_tempo_normal", 0) or 0)
    avg_energy_stress = float(insights.get("avg_energy_stress", 0) or 0)
    avg_energy_normal = float(insights.get("avg_energy_normal", 0) or 0)
    stress_behavior = insights.get(
        "stress_behavior", "No conclusion yet — run the pipeline to generate insights.json."
    )
    peak_deadline = insights.get("peak_stress_deadline")
    peak_deadline_energy = insights.get("peak_stress_deadline_energy")

    # The pipeline already computed the recommendation (recommender.py runs
    # inside load_task()), so the dashboard just displays it instead of
    # recalculating it a second time.
    mood = insights.get("mood", "unknown")
    playlist_type = insights.get("playlist_type", "n/a")
    tracks = insights.get("recommendations", [])

    accent = "#ff6b4a" if mood == "stress" else "#1db954"
    mood_label = {
        "stress": "High stress signal",
        "balanced": "Balanced signal",
    }.get(mood, "Signal unclear")

    energy_stress_pct = clamp_pct(avg_energy_stress, 0, 1)
    energy_normal_pct = clamp_pct(avg_energy_normal, 0, 1)
    tempo_stress_pct = clamp_pct(avg_tempo_stress, 60, 200)
    tempo_normal_pct = clamp_pct(avg_tempo_normal, 60, 200)

    tracks_html = "".join(
        f'<li class="track"><span class="track-index">{str(i+1).zfill(2)}</span>'
        f'<span class="track-name">{t}</span></li>'
        for i, t in enumerate(tracks)
    ) or '<li class="track track-empty">No tracks available yet.</li>'

    if peak_deadline:
        energy_str = f"{peak_deadline_energy:.2f}" if peak_deadline_energy is not None else "n/a"
        peak_html = (
            f'<div class="peak-callout">'
            f'<span class="peak-label">Peak stress moment</span>'
            f'<span class="peak-value">{peak_deadline}</span>'
            f'<span class="peak-sub">avg energy {energy_str} during that week</span>'
            f'</div>'
        )
    else:
        peak_html = ""

    bars_html = "".join(
        f'<span class="bar" style="--d:{0.6 + (i % 5) * 0.11}s;--h:{30 + (i * 37) % 60}%"></span>'
        for i in range(14)
    )

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Academic Stress Music Dashboard</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg: #121417;
                --surface: #191c20;
                --border: #2a2e33;
                --text: #edf1f0;
                --muted: #8b939b;
                --accent: {accent};
                --tempo: #4ac3d9;
                --normal: #5b636b;
            }}

            * {{ box-sizing: border-box; }}

            body {{
                margin: 0;
                background: var(--bg);
                color: var(--text);
                font-family: 'Inter', sans-serif;
            }}

            .hero {{
                padding: 56px 32px 40px;
                border-bottom: 1px solid var(--border);
                position: relative;
                overflow: hidden;
            }}

            .eq {{
                position: absolute;
                right: 32px;
                top: 50%;
                transform: translateY(-50%);
                display: flex;
                align-items: flex-end;
                gap: 5px;
                height: 60px;
                opacity: 0.55;
            }}

            .bar {{
                width: 5px;
                height: var(--h);
                background: linear-gradient(to top, var(--accent), var(--tempo));
                border-radius: 3px;
                animation: pulse 1.4s ease-in-out infinite;
                animation-duration: var(--d);
            }}

            @keyframes pulse {{
                0%, 100% {{ transform: scaleY(0.4); }}
                50% {{ transform: scaleY(1); }}
            }}

            @media (prefers-reduced-motion: reduce) {{
                .bar {{ animation: none; }}
            }}

            .eyebrow {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 12px;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                color: var(--accent);
                margin: 0 0 10px;
            }}

            h1 {{
                font-family: 'Space Grotesk', sans-serif;
                font-size: 34px;
                margin: 0;
                max-width: 640px;
                line-height: 1.15;
            }}

            .subtitle {{
                color: var(--muted);
                margin: 12px 0 0;
                max-width: 560px;
                font-size: 15px;
            }}

            .container {{
                padding: 32px;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                max-width: 1100px;
                margin: 0 auto;
            }}

            @media (max-width: 760px) {{
                .container {{ grid-template-columns: 1fr; }}
                .eq {{ display: none; }}
            }}

            .card {{
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 24px;
            }}

            .card h2 {{
                font-family: 'Space Grotesk', sans-serif;
                font-size: 15px;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                color: var(--muted);
                margin: 0 0 20px;
            }}

            .metric-block {{
                margin-bottom: 22px;
            }}

            .metric-block:last-child {{
                margin-bottom: 0;
            }}

            .metric-title {{
                font-size: 13px;
                color: var(--muted);
                margin-bottom: 10px;
            }}

            .metric-line {{
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 6px;
            }}

            .metric-tag {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 11px;
                width: 54px;
                flex-shrink: 0;
                color: var(--muted);
            }}

            .metric-tag.is-stress {{ color: var(--accent); }}

            .meter {{
                flex: 1;
                height: 8px;
                background: #0d0f11;
                border-radius: 4px;
                overflow: hidden;
                border: 1px solid var(--border);
            }}

            .meter-fill {{
                height: 100%;
                border-radius: 4px;
            }}

            .meter-fill.stress {{ background: var(--accent); }}
            .meter-fill.normal {{ background: var(--normal); }}

            .metric-value {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 13px;
                width: 64px;
                text-align: right;
                flex-shrink: 0;
            }}

            .conclusion-card {{
                grid-column: span 2;
            }}

            @media (max-width: 760px) {{
                .conclusion-card {{ grid-column: span 1; }}
            }}

            .badge {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: rgba(255,255,255,0.04);
                border: 1px solid var(--border);
                padding: 6px 12px;
                border-radius: 999px;
                font-size: 12px;
                color: var(--accent);
                margin-bottom: 16px;
            }}

            .badge::before {{
                content: "";
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: var(--accent);
            }}

            .conclusion-text {{
                font-size: 16px;
                line-height: 1.6;
                color: var(--text);
                max-width: 680px;
            }}

            .peak-callout {{
                margin-top: 18px;
                padding: 14px 18px;
                background: rgba(255,255,255,0.03);
                border-left: 3px solid var(--accent);
                border-radius: 0 8px 8px 0;
                display: flex;
                flex-direction: column;
                gap: 3px;
                max-width: 420px;
            }}

            .peak-label {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: var(--muted);
            }}

            .peak-value {{
                font-family: 'Space Grotesk', sans-serif;
                font-size: 17px;
                color: var(--accent);
            }}

            .peak-sub {{
                font-size: 13px;
                color: var(--muted);
            }}

            .rec-card {{
                grid-column: span 2;
            }}

            @media (max-width: 760px) {{
                .rec-card {{ grid-column: span 1; }}
            }}

            .playlist-type {{
                font-family: 'Space Grotesk', sans-serif;
                font-size: 20px;
                margin: 0 0 18px;
                color: var(--text);
            }}

            .playlist-type span {{
                color: var(--accent);
            }}

            .tracks {{
                list-style: none;
                margin: 0;
                padding: 0;
            }}

            .track {{
                display: flex;
                align-items: center;
                gap: 16px;
                padding: 12px 0;
                border-bottom: 1px solid var(--border);
                font-size: 15px;
            }}

            .track:last-child {{
                border-bottom: none;
            }}

            .track-index {{
                font-family: 'JetBrains Mono', monospace;
                color: var(--muted);
                font-size: 13px;
            }}

            .track-empty {{
                color: var(--muted);
                font-style: italic;
            }}

            footer {{
                text-align: center;
                color: var(--muted);
                font-size: 12px;
                padding: 24px;
            }}
        </style>
    </head>
    <body>

        <div class="hero">
            <p class="eyebrow">Academic Stress · Listening Behavior</p>
            <h1>Academic Stress Music Intelligence</h1>
            <p class="subtitle">How students' listening habits shift under academic pressure, and what to play next.</p>
            <div class="eq">{bars_html}</div>
        </div>

        <div class="container">

            <div class="card">
                <h2>Energy — Stress vs Normal</h2>
                <div class="metric-block">
                    <div class="metric-line">
                        <span class="metric-tag is-stress">STRESS</span>
                        <div class="meter"><div class="meter-fill stress" style="width:{energy_stress_pct:.0f}%"></div></div>
                        <span class="metric-value">{avg_energy_stress:.2f}</span>
                    </div>
                    <div class="metric-line">
                        <span class="metric-tag">NORMAL</span>
                        <div class="meter"><div class="meter-fill normal" style="width:{energy_normal_pct:.0f}%"></div></div>
                        <span class="metric-value">{avg_energy_normal:.2f}</span>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>Tempo — Stress vs Normal</h2>
                <div class="metric-block">
                    <div class="metric-line">
                        <span class="metric-tag is-stress">STRESS</span>
                        <div class="meter"><div class="meter-fill stress" style="width:{tempo_stress_pct:.0f}%"></div></div>
                        <span class="metric-value">{avg_tempo_stress:.1f} bpm</span>
                    </div>
                    <div class="metric-line">
                        <span class="metric-tag">NORMAL</span>
                        <div class="meter"><div class="meter-fill normal" style="width:{tempo_normal_pct:.0f}%"></div></div>
                        <span class="metric-value">{avg_tempo_normal:.1f} bpm</span>
                    </div>
                </div>
            </div>

            <div class="card conclusion-card">
                <h2>Conclusion</h2>
                <div class="badge">{mood_label}</div>
                <p class="conclusion-text">{stress_behavior}</p>
                {peak_html}
            </div>

            <div class="card rec-card">
                <h2>Recommendations</h2>
                <p class="playlist-type">Suggested playlist: <span>{playlist_type}</span></p>
                <ul class="tracks">
                    {tracks_html}
                </ul>
            </div>

        </div>

        <footer>Academic Stress Music Intelligence · generated from the Airflow pipeline output</footer>

    </body>
    </html>
    """

    return html
