"""
Script to sync all data from local database to Render remote database
This script will:
1. Connect to local database
2. Read all data from all tables
3. Connect to Render database
4. Insert all data into Render database
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# ============================================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================================

# Local database connection
LOCAL_DATABASE_URL = 'postgresql://postgres:123456@localhost/caregiver_platform'

# Render database connection - UPDATE THIS WITH YOUR RENDER DATABASE URL
# Get this from Render dashboard → PostgreSQL → Connections → External Database URL
RENDER_DATABASE_URL = input("\n📝 Enter your Render External Database URL: ").strip()

# If Render URL starts with postgres://, convert to postgresql://
if RENDER_DATABASE_URL.startswith('postgres://'):
    RENDER_DATABASE_URL = RENDER_DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# ============================================================
# SCRIPT EXECUTION
# ============================================================

def get_table_data(session, table_name):
    """Get all data from a table"""
    try:
        result = session.execute(text(f"SELECT * FROM {table_name}"))
        rows = result.fetchall()
        # Get column names from result keys (SQLAlchemy 2.0)
        columns = list(result.keys())
        return rows, columns
    except Exception as e:
        print(f"❌ Error reading {table_name}: {str(e)}")
        return [], []

def insert_table_data(session, table_name, rows, columns):
    """Insert data into a table"""
    if not rows:
        print(f"   ⚠️  No data to insert")
        return 0
    
    try:
        # First, clear existing data
        session.execute(text(f"DELETE FROM {table_name}"))
        
        # Build INSERT statement
        column_str = ', '.join(columns)
        placeholders = ', '.join([':' + col for col in columns])
        
        insert_sql = f"INSERT INTO {table_name} ({column_str}) VALUES ({placeholders})"
        
        # Insert each row
        inserted_count = 0
        for row in rows:
            row_dict = dict(zip(columns, row))
            session.execute(text(insert_sql), row_dict)
            inserted_count += 1
        
        session.commit()
        return inserted_count
    except Exception as e:
        session.rollback()
        print(f"   ❌ Error inserting data: {str(e)}")
        return 0

def sync_table(local_session, render_session, table_name, columns):
    """Sync data for a single table"""
    print(f"\n📊 Syncing {table_name}...")
    
    # Get data from local
    rows, cols = get_table_data(local_session, table_name)
    print(f"   📥 Found {len(rows)} rows in local database")
    
    if not rows:
        print(f"   ⚠️  Skipping {table_name} (no data)")
        return
    
    # Insert into Render
    count = insert_table_data(render_session, table_name, rows, cols)
    if count > 0:
        print(f"   ✅ Successfully inserted {count} rows into Render database")
    else:
        print(f"   ❌ Failed to insert data")

def main():
    print("=" * 60)
    print("🔄 Database Sync: Local → Render")
    print("=" * 60)
    
    # Create connections
    try:
        print("\n🔌 Connecting to local database...")
        local_engine = create_engine(LOCAL_DATABASE_URL, echo=False)
        local_session = sessionmaker(bind=local_engine)()
        print("   ✅ Connected to local database")
    except Exception as e:
        print(f"   ❌ Failed to connect to local database: {str(e)}")
        return
    
    try:
        print("\n🔌 Connecting to Render database...")
        render_engine = create_engine(RENDER_DATABASE_URL, echo=False)
        render_session = sessionmaker(bind=render_engine)()
        print("   ✅ Connected to Render database")
    except Exception as e:
        print(f"   ❌ Failed to connect to Render database: {str(e)}")
        print("   💡 Make sure you've updated RENDER_DATABASE_URL in the script")
        local_session.close()
        return
    
    # Define tables in order (respecting foreign key constraints)
    tables = [
        ('users', ['user_id', 'email', 'given_name', 'surname', 'city', 'phone_number', 'profile_description', 'password']),
        ('caregiver', ['caregiver_user_id', 'photo', 'gender', 'caregiving_type', 'hourly_rate']),
        ('member', ['member_user_id', 'house_rules', 'dependent_description']),
        ('address', ['member_user_id', 'house_number', 'street', 'town']),
        ('job', ['job_id', 'member_user_id', 'required_caregiving_type', 'other_requirements', 'date_posted']),
        ('job_application', ['caregiver_user_id', 'job_id', 'date_applied']),
        ('appointment', ['appointment_id', 'caregiver_user_id', 'member_user_id', 'appointment_date', 'appointment_time', 'work_hours', 'status']),
    ]
    
    # Sync each table
    total_synced = 0
    for table_name, columns in tables:
        try:
            sync_table(local_session, render_session, table_name, columns)
            total_synced += 1
        except Exception as e:
            print(f"   ❌ Error syncing {table_name}: {str(e)}")
    
    # Close connections
    local_session.close()
    render_session.close()
    
    print("\n" + "=" * 60)
    print(f"✅ Sync complete! Synced {total_synced} tables")
    print("=" * 60)
    print("\n💡 Your Render database now has all the data from your local database!")
    print("   You can verify by checking your Render database or visiting your app.")

if __name__ == "__main__":
    # Get Render database URL
    if not RENDER_DATABASE_URL or RENDER_DATABASE_URL == 'postgresql://caregive_platform_user:vhwRsWEc3IVKSzy7jXKYu90CCXdzydEy@dpg-d4jj98m3jp1c73b88meg-a.oregon-postgres.render.com/caregive_platform':
        print("\n📝 Please enter your Render External Database URL")
        print("   (Get it from Render dashboard → PostgreSQL → Connections)")
        render_url = input("Render Database URL: ").strip()
        if render_url:
            RENDER_DATABASE_URL = render_url
            if RENDER_DATABASE_URL.startswith('postgres://'):
                RENDER_DATABASE_URL = RENDER_DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    # Confirm before proceeding
    print("\n⚠️  WARNING: This will DELETE all existing data in Render database")
    print("   and replace it with data from your local database.")
    response = input("\nDo you want to continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        main()
    else:
        print("❌ Sync cancelled.")

