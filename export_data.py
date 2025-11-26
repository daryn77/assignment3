"""
Script to export data from local database and generate INSERT statements
Run this on your local machine to export data from your local PostgreSQL database
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# Local database connection
LOCAL_DATABASE_URL = 'postgresql://postgres:123456@localhost/caregiver_platform'

# Create engine
engine = create_engine(LOCAL_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def export_table_data(session, table_name, columns):
    """Export data from a table and generate INSERT statements"""
    try:
        # Get all data
        result = session.execute(text(f"SELECT * FROM {table_name}"))
        rows = result.fetchall()
        
        if not rows:
            return f"-- No data in {table_name}\n"
        
        # Get column names
        column_names = [desc[0] for desc in result.description]
        
        # Generate INSERT statements
        inserts = []
        inserts.append(f"\n-- Data for {table_name}\n")
        inserts.append(f"DELETE FROM {table_name};\n")  # Clear existing data
        
        for row in rows:
            values = []
            for val in row:
                if val is None:
                    values.append('NULL')
                elif isinstance(val, str):
                    # Escape single quotes
                    escaped_val = val.replace("'", "''")
                    values.append(f"'{escaped_val}'")
                elif isinstance(val, (int, float)):
                    values.append(str(val))
                else:
                    values.append(f"'{str(val)}'")
            
            values_str = ', '.join(values)
            column_str = ', '.join(column_names)
            inserts.append(f"INSERT INTO {table_name} ({column_str}) VALUES ({values_str});\n")
        
        return ''.join(inserts)
    except Exception as e:
        return f"-- Error exporting {table_name}: {str(e)}\n"

def main():
    session = SessionLocal()
    output = []
    
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
    
    output.append("-- Exported data from local database\n")
    output.append("-- Run this script on your Render database to import all data\n\n")
    
    for table_name, columns in tables:
        print(f"Exporting {table_name}...")
        data = export_table_data(session, table_name, columns)
        output.append(data)
        output.append("\n")
    
    session.close()
    
    # Write to file
    with open('insert_data.sql', 'w', encoding='utf-8') as f:
        f.write(''.join(output))
    
    print("\n✅ Data exported successfully to 'insert_data.sql'")
    print("You can now import this file to your Render database using:")
    print('psql "your-render-database-url" -f insert_data.sql')

if __name__ == "__main__":
    main()

