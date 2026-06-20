from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="Academic Stress & Spotify API",
    description="Analyze audio features during high-stress academic periods",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrackSelectionRequest(BaseModel):
    student_id: str
    spotify_track_id: str
    track_name: str
    artist_name: str
    week_number: int

class AudioFeaturesRequest(BaseModel):
    spotify_track_id: str
    tempo: float
    energy: float
    valence: float

class AcademicWeekRequest(BaseModel):
    week_number: int
    start_date: str
    end_date: str
    week_type: str
    project_deadline: str = None

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/tracks/log")
def log_track(request: TrackSelectionRequest):
    return {"message": "Track logged successfully", "data": request.dict()}

@app.get("/tracks/{week_number}")
def get_tracks_by_week(week_number: int):
    return {"week_number": week_number, "tracks": []}

@app.post("/audio-features")
def add_audio_features(request: AudioFeaturesRequest):
    return {"message": "Audio features stored", "data": request.dict()}

@app.get("/metrics/comparison")
def compare_audio_metrics():
    return {
        "normal_weeks": {"avg_tempo": 0, "avg_energy": 0, "sample_size": 0},
        "high_stress_weeks": {"avg_tempo": 0, "avg_energy": 0, "sample_size": 0},
        "variance_percentage": 0
    }

@app.get("/metrics/weekly/{week_number}")
def get_weekly_metrics(week_number: int):
    return {"week_number": week_number, "avg_tempo": 0, "avg_energy": 0, "track_count": 0}

@app.post("/calendar/add-week")
def add_academic_week(request: AcademicWeekRequest):
    return {"message": "Academic week added", "data": request.dict()}

@app.get("/calendar")
def get_academic_calendar():
    return {"weeks": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
