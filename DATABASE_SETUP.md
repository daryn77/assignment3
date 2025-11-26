# Database Setup Guide for Render.com

This guide will help you create and connect your PostgreSQL database on Render.com.

## Step 1: Create PostgreSQL Database on Render.com

1. **Log in to Render.com** and go to your dashboard
2. Click **"New +"** button → Select **"PostgreSQL"**
3. Fill in the database configuration:
   - **Name**: `caregiver-platform-db` (or any name you prefer)
   - **Database**: `caregiver_platform` (or leave default)
   - **User**: Auto-generated (you can't change this)
   - **Region**: Choose the same region as your web service (important for performance)
   - **PostgreSQL Version**: Latest (14 or 15)
   - **Plan**: 
     - **Free**: For testing (spins down after inactivity)
     - **Starter ($7/month)**: For production (always on)
4. Click **"Create Database"**
5. Wait for the database to be created (takes 1-2 minutes)

## Step 2: Get Database Connection String

1. Once the database is created, click on it to open the dashboard
2. Go to the **"Connections"** or **"Info"** tab
3. You'll see several connection strings:
   - **Internal Database URL** - Use this one! (for services on Render)
   - External Database URL (for connecting from outside Render)
4. **Copy the Internal Database URL** - it looks like:
   ```
   postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com/caregiver_platform
   ```

## Step 3: Set Environment Variable in Web Service

1. Go to your **Web Service** dashboard on Render.com
2. Click on **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the **Internal Database URL** you copied in Step 2
5. Click **"Save Changes"**
6. Render will automatically redeploy your service

## Step 4: Import Your Database Schema

You need to import your database tables and structure. You have two options:

### Option A: Using pgAdmin or psql (Recommended)

1. Get the **External Database URL** from your Render PostgreSQL dashboard
2. Connect using pgAdmin or psql:
   ```bash
   psql "postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com/caregiver_platform"
   ```
3. Run your SQL scripts to create tables (from Part 1 of your assignment)

### Option B: Using Python Script

1. Create a script to import your schema
2. Or use the SQL dump from your local database

### Option C: Export from Local and Import to Render

1. **Export your local database**:
   ```bash
   pg_dump -h localhost -U postgres -d caregiver_platform > database_backup.sql
   ```

2. **Import to Render database**:
   ```bash
   psql "postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com/caregiver_platform" < database_backup.sql
   ```

## Step 5: Verify Connection

1. After setting the DATABASE_URL environment variable, Render will redeploy
2. Check the logs in your Web Service dashboard
3. If you see no connection errors, the database is connected!
4. Visit your app URL and test creating a record

## Quick SQL Script to Create Tables

If you need to recreate your tables, here's a basic structure (adjust based on your actual schema):

```sql
-- Create USER table
CREATE TABLE users (
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
CREATE TABLE caregiver (
    caregiver_user_id INTEGER PRIMARY KEY,
    photo VARCHAR(255),
    gender VARCHAR(50),
    caregiving_type VARCHAR(100) NOT NULL,
    hourly_rate DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (caregiver_user_id) REFERENCES users(user_id)
);

-- Create MEMBER table
CREATE TABLE member (
    member_user_id INTEGER PRIMARY KEY,
    house_rules TEXT,
    dependent_description TEXT,
    FOREIGN KEY (member_user_id) REFERENCES users(user_id)
);

-- Create ADDRESS table
CREATE TABLE address (
    member_user_id INTEGER PRIMARY KEY,
    house_number VARCHAR(50),
    street VARCHAR(255),
    town VARCHAR(255),
    FOREIGN KEY (member_user_id) REFERENCES member(member_user_id)
);

-- Create JOB table
CREATE TABLE job (
    job_id SERIAL PRIMARY KEY,
    member_user_id INTEGER NOT NULL,
    required_caregiving_type VARCHAR(100) NOT NULL,
    other_requirements TEXT,
    date_posted DATE,
    FOREIGN KEY (member_user_id) REFERENCES member(member_user_id)
);

-- Create JOB_APPLICATION table
CREATE TABLE job_application (
    caregiver_user_id INTEGER,
    job_id INTEGER,
    date_applied DATE,
    PRIMARY KEY (caregiver_user_id, job_id),
    FOREIGN KEY (caregiver_user_id) REFERENCES caregiver(caregiver_user_id),
    FOREIGN KEY (job_id) REFERENCES job(job_id)
);

-- Create APPOINTMENT table
CREATE TABLE appointment (
    appointment_id SERIAL PRIMARY KEY,
    caregiver_user_id INTEGER NOT NULL,
    member_user_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    work_hours DECIMAL(5,2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (caregiver_user_id) REFERENCES caregiver(caregiver_user_id),
    FOREIGN KEY (member_user_id) REFERENCES member(member_user_id)
);
```

## Troubleshooting

### Error: "Connection refused"
- **Solution**: Make sure you're using the **Internal Database URL** (not external)
- Make sure DATABASE_URL environment variable is set correctly
- Verify database and web service are in the same region

### Error: "Database does not exist"
- **Solution**: Check the database name in your connection string matches the actual database name

### Error: "Password authentication failed"
- **Solution**: Make sure you copied the entire connection string correctly
- The password in the URL is URL-encoded, don't modify it

### Tables not found
- **Solution**: You need to import/create your database schema first
- Use one of the methods in Step 4 above

## Important Notes

- **Free tier databases** on Render spin down after 15 minutes of inactivity
- First connection after spin-down may take 30-60 seconds
- For production, consider upgrading to a paid plan
- Always backup your database before making changes

## Next Steps

1. Create the PostgreSQL database on Render
2. Set the DATABASE_URL environment variable
3. Import your database schema
4. Test your application!

