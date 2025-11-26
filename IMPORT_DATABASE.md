# How to Import Database Schema to Render.com

## Where to Run the Command

You can run the psql command from your **local computer's terminal/command prompt**.

## Prerequisites

1. **Install PostgreSQL client tools** (if not already installed):
   - Download from: https://www.postgresql.org/download/windows/
   - Or use the PostgreSQL installation you already have
   - Make sure `psql` is in your PATH

2. **Get your Render database connection string**:
   - Go to your Render PostgreSQL dashboard
   - Click on "Connections" tab
   - Copy the **External Database URL** (not Internal)
   - It looks like: `postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com/caregiver_platform`

## Method 1: Using Command Prompt/PowerShell (Windows)

1. **Open Command Prompt or PowerShell** on your Windows computer
2. **Navigate to your project folder**:
   ```bash
   cd C:\db_assignment
   ```

3. **Run the import command**:
   ```bash
   psql "postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com/caregiver_platform" -f create_tables.sql
   ```
   
   Replace the connection string with your actual External Database URL from Render.

4. **Or run SQL directly**:
   ```bash
   psql "postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com/caregiver_platform"
   ```
   Then copy and paste the contents of `create_tables.sql` into the psql prompt.

## Method 2: Using pgAdmin (Easier - GUI Method)

1. **Open pgAdmin** (if you have it installed)
2. **Add New Server**:
   - Right-click "Servers" → "Register" → "Server"
   - **General Tab**: Name it "Render Database"
   - **Connection Tab**:
     - **Host**: Copy from your External Database URL (e.g., `dpg-xxxxx-a.oregon-postgres.render.com`)
     - **Port**: Usually `5432`
     - **Database**: `caregiver_platform` (or whatever your database name is)
     - **Username**: From your connection URL
     - **Password**: From your connection URL
   - Click "Save"

3. **Connect to the server**
4. **Right-click on your database** → "Query Tool"
5. **Open `create_tables.sql`** file and copy all contents
6. **Paste into Query Tool** and click "Execute" (F5)

## Method 3: Using Render's Built-in Terminal (If Available)

Some Render plans include a web terminal:
1. Go to your PostgreSQL database dashboard on Render
2. Look for "Shell" or "Terminal" option
3. If available, you can run commands there

## Method 4: Using Python Script (Alternative)

Create a Python script to run the SQL:

```python
import psycopg2
import os

# Get connection string from environment or paste it here
DATABASE_URL = "postgresql://user:password@host/database"

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Read and execute SQL file
with open('create_tables.sql', 'r') as f:
    cur.execute(f.read())

conn.commit()
cur.close()
conn.close()
print("Tables created successfully!")
```

## Step-by-Step Example (Command Prompt)

1. Open **Command Prompt** (Win + R, type `cmd`, Enter)

2. Navigate to your project:
   ```
   cd C:\db_assignment
   ```

3. Check if psql is installed:
   ```
   psql --version
   ```
   If you get an error, you need to install PostgreSQL client tools.

4. Get your External Database URL from Render dashboard

5. Run the import:
   ```
   psql "postgresql://your-connection-string-here" -f create_tables.sql
   ```

6. You'll be prompted for password (if not in URL) or it will execute directly

## Troubleshooting

### "psql is not recognized"
- Install PostgreSQL from https://www.postgresql.org/download/windows/
- Or add PostgreSQL bin folder to your PATH:
  - Usually: `C:\Program Files\PostgreSQL\15\bin`
  - Add to System Environment Variables → Path

### "Connection refused"
- Make sure you're using the **External Database URL** (not Internal)
- Check that your database is running on Render
- Verify the connection string is correct

### "Database does not exist"
- The database name in the URL should match your Render database name
- Check your Render database dashboard for the correct name

## Recommended Method

**For beginners**: Use **pgAdmin** (Method 2) - it's the easiest with a visual interface.

**For advanced users**: Use **Command Prompt** (Method 1) - faster and more direct.

