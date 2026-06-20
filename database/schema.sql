-- Academic Calendar Table
CREATE TABLE academic_calendar (
    id SERIAL PRIMARY KEY,
    week_number INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    week_type VARCHAR(20) NOT NULL,
    project_deadline VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Students Table
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    spotify_user_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Track Selections
CREATE TABLE track_selections (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(id),
    spotify_track_id VARCHAR(100) NOT NULL,
    track_name VARCHAR(255) NOT NULL,
    artist_name VARCHAR(255) NOT NULL,
    week_number INT NOT NULL REFERENCES academic_calendar(week_number),
    logged_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Audio Features
CREATE TABLE audio_features (
    id SERIAL PRIMARY KEY,
    spotify_track_id VARCHAR(100) UNIQUE NOT NULL,
    tempo FLOAT NOT NULL,
    energy FLOAT NOT NULL,
    valence FLOAT NOT NULL,
    danceability FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    speechiness FLOAT,
    loudness FLOAT,
    fetched_at TIMESTAMP DEFAULT NOW()
);

-- Weekly Aggregated Metrics
CREATE TABLE weekly_metrics (
    id SERIAL PRIMARY KEY,
    week_number INT NOT NULL,
    week_type VARCHAR(20) NOT NULL,
    avg_tempo FLOAT,
    avg_energy FLOAT,
    avg_valence FLOAT,
    track_count INT,
    student_count INT,
    calculated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(week_number, week_type)
);

-- Indexes
CREATE INDEX idx_track_selections_week ON track_selections(week_number);
CREATE INDEX idx_audio_features_track ON audio_features(spotify_track_id);
CREATE INDEX idx_weekly_metrics_week_type ON weekly_metrics(week_type);
