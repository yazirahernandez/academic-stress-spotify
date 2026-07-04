from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    try:
        with open("data/insights.json") as f:
            insights = json.load(f)
    except:
        insights = {"avg_tempo": 0, "avg_energy": 0}

    html = f"""
    <html>
    <head>
        <title>Music Stress Dashboard</title>
        <style>
            body {{ font-family: Arial; background:#111; color:white; padding:40px; }}
            .card {{ background:#222; padding:20px; border-radius:10px; margin:10px; }}
            h1 {{ color:#1db954; }}
        </style>
    </head>
    <body>

        <h1>🎧 Academic Stress Dashboard</h1>

        <div class="card">
            <h2>📊 Insights</h2>
            <p>Avg Tempo: {insights['avg_tempo']}</p>
            <p>Avg Energy: {insights['avg_energy']}</p>
        </div>

        <div class="card">
            <h2>🧠 Insight</h2>
            <p>Students show different audio behavior under stress conditions.</p>
        </div>

    </body>
    </html>
    """

    return html
