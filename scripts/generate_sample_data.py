import pandas as pd
import json
import random
from datetime import datetime, timedelta
import os

def generate_academic_calendar():
    data = []
    start_date = datetime(2024, 1, 8)
    
    for week in range(1, 17):
        week_type = "high-stress" if week in [3, 7, 10, 14] else "normal"
        project_deadline = f"Project {week//3 + 1} Deadline" if week_type == "high-stress" else None
        
        data.append({
            "week_number": week,
            "start_date": (start_date + timedelta(weeks=week-1)).strftime("%Y-%m-%d"),
            "end_date": (start_date + timedelta(weeks=week)).strftime("%Y-%m-%d"),
            "week_type": week_type,
            "project_deadline": project_deadline
        })
    
    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/academic_calendar.csv", index=False)
    print("✅ Academic calendar generated")

def generate_student_list():
    students = []
    for i in range(1, 51):
        students.append({
            "student_id": f"STU{i:03d}",
            "name": f"Student {i}",
            "email": f"student{i}@university.edu",
            "spotify_user_id": f"spotify_user_{i}"
        })
    
    df = pd.DataFrame(students)
    df.to_csv("data/students.csv", index=False)
    print("✅ Student list generated")

def generate_track_selections():
    tracks = []
    
    high_stress_tracks = [
        ("track_hs_001", "Eye of the Tiger", "Survivor", 0.96, 0.51),
        ("track_hs_002", "Pumped Up Kicks", "Foster the People", 0.75, 0.49),
    ]
    
    normal_tracks = [
        ("track_nm_001", "Blinding Lights", "The Weeknd", 0.73, 0.64),
        ("track_nm_002", "Good as Hell", "Lizzo", 0.68, 0.85),
    ]
    
    for student_id in range(1, 51):
        for week in range(1, 17):
            week_type = "high-stress" if week in [3, 7, 10, 14] else "normal"
            
            if week_type == "high-stress":
                track_id, name, artist, energy, valence = random.choice(high_stress_tracks)
            else:
                track_id, name, artist, energy, valence = random.choice(normal_tracks)
            
            tracks.append({
                "student_id": f"STU{student_id:03d}",
                "week_number": week,
                "week_type": week_type,
                "spotify_track_id": track_id,
                "track_name": name,
                "artist_name": artist,
                "energy": energy,
                "valence": valence
            })
    
    df = pd.DataFrame(tracks)
    df.to_csv("data/track_selections.csv", index=False)
    print("✅ Track selections generated")

if __name__ == "__main__":
    generate_academic_calendar()
    generate_student_list()
    generate_track_selections()
    print("\n✅ All sample data generated!")
