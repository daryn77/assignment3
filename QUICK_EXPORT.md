# Quick Data Export/Import Guide

## Simplest Method: Using pgAdmin (Easiest!)

### Step 1: Export from Local Database (pgAdmin)

1. **Open pgAdmin** and connect to your local database
2. **Right-click on your database** → "Backup"
3. **Settings**:
   - Filename: `caregiver_platform_backup.sql`
   - Format: **Plain**
   - Encoding: **UTF8**
   - **Dump Options** tab:
     - ✅ **Data Only** (uncheck "Schema Only")
     - ✅ **Column Inserts** (this creates INSERT statements)
     - ✅ **Use INSERT commands**
4. Click **"Backup"**
5. Wait for backup to complete

### Step 2: Import to Render Database (pgAdmin)

1. **Connect to your Render database** in pgAdmin
2. **Right-click on your database** → "Query Tool"
3. **Open the backup file** you just created
4. **Copy all the INSERT statements** (skip the SET commands at the top)
5. **Paste into Query Tool**
6. **Click "Execute" (F5)**
7. Done! ✅

## Alternative: Using psql Command Line

### Step 1: Connect to Local Database

```bash
psql -h localhost -U postgres -d caregiver_platform
```

### Step 2: Generate INSERT Statements

In the psql prompt, run:

```sql
-- First, clear output to file
\o insert_statements.sql

-- Generate INSERT for users
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

-- Repeat for other tables (caregiver, member, address, job, job_application, appointment)
-- Use the same pattern, adjusting column names

-- Stop output to file
\o
\q
```

### Step 3: Import to Render

```bash
psql "your-render-database-url" -f insert_statements.sql
```

## Even Simpler: Manual Copy from pgAdmin

1. **For each table** in pgAdmin:
   - Right-click table → "View/Edit Data" → "All Rows"
   - Right-click on the data grid → "Copy" → "Copy as SQL INSERT"
   - Paste into a text file

2. **Connect to Render database** in pgAdmin
3. **Open Query Tool**
4. **Paste all INSERT statements** (in order: users, caregiver, member, address, job, job_application, appointment)
5. **Execute**

## Recommended Order for Import

Import tables in this order to avoid foreign key errors:

1. ✅ **users** (no dependencies)
2. ✅ **caregiver** (depends on users)
3. ✅ **member** (depends on users)
4. ✅ **address** (depends on member)
5. ✅ **job** (depends on member)
6. ✅ **job_application** (depends on caregiver and job)
7. ✅ **appointment** (depends on caregiver and member)

