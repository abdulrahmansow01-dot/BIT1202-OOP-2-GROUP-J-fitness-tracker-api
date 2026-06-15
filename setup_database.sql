-- Copy and paste these commands in PostgreSQL to set up the database

CREATE DATABASE fitness_tracker;
CREATE USER postgres WITH PASSWORD '654123';
GRANT ALL PRIVILEGES ON DATABASE fitness_tracker TO postgres;

-- Connect to the database
\c fitness_tracker

-- Create tables
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_superuser BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    duration_minutes INTEGER NOT NULL,
    calories_burned INTEGER NOT NULL,
    owner_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE nutrition_entries (
    id SERIAL PRIMARY KEY,
    meal_type VARCHAR(60) NOT NULL,
    description TEXT,
    calories INTEGER NOT NULL,
    protein_grams FLOAT NOT NULL,
    carbohydrates_grams FLOAT NOT NULL,
    fats_grams FLOAT NOT NULL,
    date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    owner_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE progress_entries (
    id SERIAL PRIMARY KEY,
    weight_kg FLOAT NOT NULL,
    body_fat_percentage FLOAT,
    notes TEXT,
    date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    owner_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Grant privileges on tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
