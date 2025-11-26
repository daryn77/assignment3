# Export and Import Data Guide

This guide will help you export data from your local database and import it into your Render database.

## Method 1: Using Python Script (Recommended)

### Step 1: Export Data from Local Database

1. **Make sure your local database is running** and has all your data

2. **Update the connection string** in `export_data.py` if needed:
   ```python
   LOCAL_DATABASE_URL = 'postgresql://postgres:123456@localhost/caregiver_platform'
   ```

3. **Run the export script**:
   ```bash
   python export_data.py
   ```

4. This will create a file called `insert_data.sql` with all your data

### Step 2: Import Data to Render Database

1. **Get your Render External Database URL** from Render dashboard

2. **Run the import command**:
   ```bash
   psql "postgresql://user:password@host/database" -f insert_data.sql
   ```

   Replace with your actual Render database URL.

## Method 2: Using pg_dump (Command Line)

### Step 1: Export Data Only (No Schema)

```bash
pg_dump -h localhost -U postgres -d caregiver_platform --data-only --column-inserts > data_export.sql
```

This creates INSERT statements for all your data.

### Step 2: Import to Render

```bash
psql "your-render-database-url" -f data_export.sql
```

## Method 3: Using pgAdmin

### Step 1: Export from Local Database

1. Connect to your local database in pgAdmin
2. Right-click on your database → "Backup"
3. Select:
   - Format: "Plain"
   - Encoding: "UTF8"
   - Dump Options → Data Only: ✅ Check
   - Dump Options → Column Inserts: ✅ Check
4. Click "Backup"
5. Save the file

### Step 2: Import to Render Database

1. Connect to your Render database in pgAdmin
2. Right-click on your database → "Query Tool"
3. Open the exported SQL file
4. Copy all contents
5. Paste into Query Tool
6. Click "Execute" (F5)

## Method 4: Manual Export/Import (For Small Amounts of Data)

### Step 1: Export Each Table

In pgAdmin, for each table:
1. Right-click table → "View/Edit Data" → "All Rows"
2. Right-click on data → "Copy" → "Copy as SQL INSERT"
3. Paste into a text file

### Step 2: Import

1. Connect to Render database
2. Open Query Tool
3. Paste the INSERT statements
4. Execute

## Quick Commands Summary

### Export from Local:
```bash
# Using Python script
python export_data.py

# Using pg_dump (data only)
pg_dump -h localhost -U postgres -d caregiver_platform --data-only --column-inserts > data.sql
```

### Import to Render:
```bash
psql "postgresql://user:pass@host/db" -f insert_data.sql
```

## Troubleshooting

### "Permission denied" or "Access denied"
- Make sure you're using the correct username and password
- Check that your local PostgreSQL is running

### "Table does not exist"
- Make sure you've already created the tables on Render (run `create_tables.sql` first)
- Check table names match exactly

### "Foreign key constraint violation"
- Make sure you import data in the correct order:
  1. users
  2. caregiver
  3. member
  4. address
  5. job
  6. job_application
  7. appointment

### "Duplicate key error"
- The script includes `DELETE FROM` statements to clear existing data
- If you get duplicate errors, the data might already be imported

## Verify Import

After importing, check your data:

```sql
-- In psql or pgAdmin Query Tool
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM caregiver;
SELECT COUNT(*) FROM member;
-- etc.
```

You should see the same number of rows as in your local database.

