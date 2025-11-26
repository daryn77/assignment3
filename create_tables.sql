-- Database Schema for Caregiver Platform
-- Run this script on your Render PostgreSQL database to create all tables

-- Create USER table
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    given_name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    city VARCHAR(255),
    phone_number VARCHAR(50),
    profile_description TEXT,
    password VARCHAR(255) NOT NULL
);

-- Create CAREGIVER table
CREATE TABLE IF NOT EXISTS caregiver (
    caregiver_user_id INTEGER PRIMARY KEY,
    photo VARCHAR(255),
    gender VARCHAR(50),
    caregiving_type VARCHAR(100) NOT NULL,
    hourly_rate DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (caregiver_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create MEMBER table
CREATE TABLE IF NOT EXISTS member (
    member_user_id INTEGER PRIMARY KEY,
    house_rules TEXT,
    dependent_description TEXT,
    FOREIGN KEY (member_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create ADDRESS table
CREATE TABLE IF NOT EXISTS address (
    member_user_id INTEGER PRIMARY KEY,
    house_number VARCHAR(50),
    street VARCHAR(255),
    town VARCHAR(255),
    FOREIGN KEY (member_user_id) REFERENCES member(member_user_id) ON DELETE CASCADE
);

-- Create JOB table
CREATE TABLE IF NOT EXISTS job (
    job_id SERIAL PRIMARY KEY,
    member_user_id INTEGER NOT NULL,
    required_caregiving_type VARCHAR(100) NOT NULL,
    other_requirements TEXT,
    date_posted DATE,
    FOREIGN KEY (member_user_id) REFERENCES member(member_user_id) ON DELETE CASCADE
);

-- Create JOB_APPLICATION table
CREATE TABLE IF NOT EXISTS job_application (
    caregiver_user_id INTEGER,
    job_id INTEGER,
    date_applied DATE,
    PRIMARY KEY (caregiver_user_id, job_id),
    FOREIGN KEY (caregiver_user_id) REFERENCES caregiver(caregiver_user_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job(job_id) ON DELETE CASCADE
);

-- Create APPOINTMENT table
CREATE TABLE IF NOT EXISTS appointment (
    appointment_id SERIAL PRIMARY KEY,
    caregiver_user_id INTEGER NOT NULL,
    member_user_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    work_hours DECIMAL(5,2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (caregiver_user_id) REFERENCES caregiver(caregiver_user_id) ON DELETE CASCADE,
    FOREIGN KEY (member_user_id) REFERENCES member(member_user_id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_caregiver_type ON caregiver(caregiving_type);
CREATE INDEX IF NOT EXISTS idx_job_type ON job(required_caregiving_type);
CREATE INDEX IF NOT EXISTS idx_appointment_date ON appointment(appointment_date);
CREATE INDEX IF NOT EXISTS idx_appointment_status ON appointment(status);

