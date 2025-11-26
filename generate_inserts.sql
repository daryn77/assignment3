-- Run this in your LOCAL database psql prompt to generate INSERT statements
-- Connect to local database first: psql -h localhost -U postgres -d caregiver_platform

-- Then copy the output and run it on Render database

\echo '-- Exporting users table'
SELECT 'INSERT INTO users (user_id, email, given_name, surname, city, phone_number, profile_description, password) VALUES (' ||
    user_id || ', ' ||
    quote_literal(email) || ', ' ||
    quote_literal(given_name) || ', ' ||
    quote_literal(surname) || ', ' ||
    COALESCE(quote_literal(city), 'NULL') || ', ' ||
    COALESCE(quote_literal(phone_number), 'NULL') || ', ' ||
    COALESCE(quote_literal(profile_description), 'NULL') || ', ' ||
    quote_literal(password) || ');'
FROM users;

\echo '-- Exporting caregiver table'
SELECT 'INSERT INTO caregiver (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) VALUES (' ||
    caregiver_user_id || ', ' ||
    COALESCE(quote_literal(photo), 'NULL') || ', ' ||
    COALESCE(quote_literal(gender), 'NULL') || ', ' ||
    quote_literal(caregiving_type) || ', ' ||
    hourly_rate || ');'
FROM caregiver;

\echo '-- Exporting member table'
SELECT 'INSERT INTO member (member_user_id, house_rules, dependent_description) VALUES (' ||
    member_user_id || ', ' ||
    COALESCE(quote_literal(house_rules), 'NULL') || ', ' ||
    COALESCE(quote_literal(dependent_description), 'NULL') || ');'
FROM member;

\echo '-- Exporting address table'
SELECT 'INSERT INTO address (member_user_id, house_number, street, town) VALUES (' ||
    member_user_id || ', ' ||
    COALESCE(quote_literal(house_number), 'NULL') || ', ' ||
    COALESCE(quote_literal(street), 'NULL') || ', ' ||
    COALESCE(quote_literal(town), 'NULL') || ');'
FROM address;

\echo '-- Exporting job table'
SELECT 'INSERT INTO job (job_id, member_user_id, required_caregiving_type, other_requirements, date_posted) VALUES (' ||
    job_id || ', ' ||
    member_user_id || ', ' ||
    quote_literal(required_caregiving_type) || ', ' ||
    COALESCE(quote_literal(other_requirements), 'NULL') || ', ' ||
    COALESCE(quote_literal(date_posted::text), 'NULL') || ');'
FROM job;

\echo '-- Exporting job_application table'
SELECT 'INSERT INTO job_application (caregiver_user_id, job_id, date_applied) VALUES (' ||
    caregiver_user_id || ', ' ||
    job_id || ', ' ||
    COALESCE(quote_literal(date_applied::text), 'NULL') || ');'
FROM job_application;

\echo '-- Exporting appointment table'
SELECT 'INSERT INTO appointment (appointment_id, caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) VALUES (' ||
    appointment_id || ', ' ||
    caregiver_user_id || ', ' ||
    member_user_id || ', ' ||
    quote_literal(appointment_date::text) || ', ' ||
    quote_literal(appointment_time::text) || ', ' ||
    work_hours || ', ' ||
    quote_literal(status) || ');'
FROM appointment;

