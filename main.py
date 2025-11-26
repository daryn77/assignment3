from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ============================================================
# 1. DATABASE CONNECTION CONFIGURATION
# ============================================================

# Database connection string
DATABASE_URL = 'postgresql://postgres:123456@localhost/caregiver_platform'

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ============================================================
# 2. SQL OPERATIONS IMPLEMENTATION
# ============================================================

def print_separator(title):
    """Helper function to print section separators"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def print_results(results, description):
    """Helper function to print query results"""
    print(f"\n{description}:")
    print("-" * 80)
    if not results:
        print("No results found.")
    else:
        for row in results:
            print(row)
    print()


def main():
    """Main function to execute all SQL operations"""
    session = SessionLocal()
    
    try:
        # ============================================================
        # 3. UPDATE QUERIES
        # ============================================================
        print_separator("3. UPDATE QUERIES")
        
        # 3.1 Update phone number of Arman Armanov
        print("3.1 Updating phone number of Arman Armanov to +77773414141...")
        try:
            result = session.execute(
                text("""
                    UPDATE users 
                    SET phone_number = '+77773414141'
                    WHERE given_name = 'Arman' AND surname = 'Armanov'
                """)
            )
            session.commit()
            print(f"✓ Updated {result.rowcount} record(s)")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # 3.2 Add commission fee to caregivers
        print("\n3.2 Adding commission fee to caregivers...")
        try:
            result = session.execute(
                text("""
                    UPDATE caregiver
                    SET hourly_rate = CASE
                        WHEN hourly_rate < 10 THEN hourly_rate + 0.3
                        ELSE hourly_rate * 1.10
                    END
                """)
            )
            session.commit()
            print(f"✓ Updated {result.rowcount} caregiver(s)")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # ============================================================
        # 4. DELETE QUERIES
        # ============================================================
        print_separator("4. DELETE QUERIES")
        
        # 4.1 Delete jobs posted by Amina Aminova
        print("4.1 Deleting jobs posted by Amina Aminova...")
        try:
            # First delete job applications that reference these jobs
            result1 = session.execute(
                text("""
                    DELETE FROM job_application
                    WHERE job_id IN (
                        SELECT job_id
                        FROM job
                        WHERE member_user_id IN (
                            SELECT member_user_id
                            FROM member
                            JOIN users ON member.member_user_id = users.user_id
                            WHERE users.given_name = 'Amina' AND users.surname = 'Aminova'
                        )
                    )
                """)
            )
            # Then delete the jobs
            result2 = session.execute(
                text("""
                    DELETE FROM job
                    WHERE member_user_id IN (
                        SELECT member_user_id
                        FROM member
                        JOIN users ON member.member_user_id = users.user_id
                        WHERE users.given_name = 'Amina' AND users.surname = 'Aminova'
                    )
                """)
            )
            session.commit()
            print(f"✓ Deleted {result1.rowcount} job application(s) and {result2.rowcount} job(s)")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # 4.2 Delete members living on Kabanbay Batyr street
        print("\n4.2 Deleting members living on Kabanbay Batyr street...")
        try:
            # First, get the member_user_ids BEFORE deleting anything
            member_ids_result = session.execute(
                text("""
                    SELECT member_user_id
                    FROM address
                    WHERE street = 'Kabanbay Batyr'
                """)
            ).fetchall()
            member_ids = [row[0] for row in member_ids_result]
            
            if member_ids:
                # Delete in order: job_application -> job -> appointment -> address -> member
                
                # 1. Delete job applications for jobs posted by these members
                result_ja = session.execute(
                    text("""
                        DELETE FROM job_application
                        WHERE job_id IN (
                            SELECT job_id
                            FROM job
                            WHERE member_user_id = ANY(:member_ids)
                        )
                    """),
                    {"member_ids": member_ids}
                )
                
                # 2. Delete jobs posted by these members
                result_job = session.execute(
                    text("""
                        DELETE FROM job
                        WHERE member_user_id = ANY(:member_ids)
                    """),
                    {"member_ids": member_ids}
                )
                
                # 3. Delete appointments with these members
                result_appt = session.execute(
                    text("""
                        DELETE FROM appointment
                        WHERE member_user_id = ANY(:member_ids)
                    """),
                    {"member_ids": member_ids}
                )
                
                # 4. Delete addresses
                result_addr = session.execute(
                    text("""
                        DELETE FROM address
                        WHERE street = 'Kabanbay Batyr'
                    """)
                )
                
                # 5. Delete members
                result_member = session.execute(
                    text("""
                        DELETE FROM member
                        WHERE member_user_id = ANY(:member_ids)
                    """),
                    {"member_ids": member_ids}
                )
                
                session.commit()
                print(f"✓ Deleted {result_ja.rowcount} job application(s), {result_job.rowcount} job(s), "
                      f"{result_appt.rowcount} appointment(s), {result_addr.rowcount} address(es), "
                      f"and {result_member.rowcount} member(s)")
            else:
                session.commit()
                print("No members found on Kabanbay Batyr street")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # ============================================================
        # 5. SIMPLE QUERIES
        # ============================================================
        print_separator("5. SIMPLE QUERIES")
        
        # 5.1 Select caregiver and member names for accepted appointments
        print("5.1 Caregiver and member names for accepted appointments:")
        try:
            results = session.execute(
                text("""
                    SELECT 
                        cg.caregiver_user_id AS caregiver_id,
                        u_cg.given_name || ' ' || u_cg.surname AS caregiver_name,
                        m.member_user_id AS member_id,
                        u_m.given_name || ' ' || u_m.surname AS member_name
                    FROM appointment a
                    JOIN caregiver cg ON a.caregiver_user_id = cg.caregiver_user_id
                    JOIN users u_cg ON cg.caregiver_user_id = u_cg.user_id
                    JOIN member m ON a.member_user_id = m.member_user_id
                    JOIN users u_m ON m.member_user_id = u_m.user_id
                    WHERE a.status = 'accepted'
                """)
            ).fetchall()
            print_results(results, "Accepted Appointments")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # 5.2 List job_ids containing 'soft-spoken' in other_requirements
        print("5.2 Job IDs with 'soft-spoken' in other_requirements:")
        try:
            results = session.execute(
                text("""
                    SELECT job_id, other_requirements
                    FROM job
                    WHERE other_requirements LIKE '%soft-spoken%'
                """)
            ).fetchall()
            print_results(results, "Jobs with 'soft-spoken' requirement")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # 5.3 List work_hours of all babysitter positions
        print("5.3 Work hours of all babysitter positions:")
        try:
            results = session.execute(
                text("""
                    SELECT 
                        a.appointment_id,
                        a.work_hours,
                        a.appointment_date,
                        a.appointment_time
                    FROM appointment a
                    JOIN caregiver cg ON a.caregiver_user_id = cg.caregiver_user_id
                    WHERE cg.caregiving_type = 'babysitter'
                """)
            ).fetchall()
            print_results(results, "Babysitter Work Hours")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # 5.4 List members looking for Elderly Care in Astana with "No pets." rule
        print("5.4 Members looking for Elderly Care in Astana with 'No pets.' rule:")
        try:
            results = session.execute(
                text("""
                    SELECT 
                        m.member_user_id,
                        u.given_name || ' ' || u.surname AS member_name,
                        u.city,
                        m.house_rules
                    FROM member m
                    JOIN users u ON m.member_user_id = u.user_id
                    JOIN job j ON m.member_user_id = j.member_user_id
                    WHERE j.required_caregiving_type = 'Elderly Care'
                      AND u.city = 'Astana'
                      AND m.house_rules LIKE '%No pets.%'
                """)
            ).fetchall()
            print_results(results, "Members in Astana seeking Elderly Care with 'No pets.' rule")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # ============================================================
        # 6. COMPLEX QUERIES
        # ============================================================
        print_separator("6. COMPLEX QUERIES")
        
        # 6.1 Count applicants for each job posted by a member
        print("6.1 Number of applicants for each job:")
        try:
            results = session.execute(
                text("""
                    SELECT 
                        j.job_id,
                        u.given_name || ' ' || u.surname AS member_name,
                        j.required_caregiving_type,
                        COUNT(ja.caregiver_user_id) AS applicant_count
                    FROM job j
                    JOIN member m ON j.member_user_id = m.member_user_id
                    JOIN users u ON m.member_user_id = u.user_id
                    LEFT JOIN job_application ja ON j.job_id = ja.job_id
                    GROUP BY j.job_id, u.given_name, u.surname, j.required_caregiving_type
                    ORDER BY j.job_id
                """)
            ).fetchall()
            print_results(results, "Job Applicants Count")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # 6.2 Total hours spent by caregivers for all accepted appointments
        print("6.2 Total hours spent by caregivers for accepted appointments:")
        try:
            results = session.execute(
                text("""
                    SELECT 
                        cg.caregiver_user_id,
                        u.given_name || ' ' || u.surname AS caregiver_name,
                        SUM(a.work_hours) AS total_hours
                    FROM appointment a
                    JOIN caregiver cg ON a.caregiver_user_id = cg.caregiver_user_id
                    JOIN users u ON cg.caregiver_user_id = u.user_id
                    WHERE a.status = 'accepted'
                    GROUP BY cg.caregiver_user_id, u.given_name, u.surname
                    ORDER BY total_hours DESC
                """)
            ).fetchall()
            print_results(results, "Total Hours by Caregiver (Accepted Appointments)")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # 6.3 Average pay of caregivers based on accepted appointments
        print("6.3 Average pay of caregivers based on accepted appointments:")
        try:
            results = session.execute(
                text("""
                    SELECT 
                        AVG(cg.hourly_rate) AS average_hourly_rate
                    FROM appointment a
                    JOIN caregiver cg ON a.caregiver_user_id = cg.caregiver_user_id
                    WHERE a.status = 'accepted'
                """)
            ).fetchall()
            print_results(results, "Average Hourly Rate (Accepted Appointments)")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # 6.4 Caregivers who earn above average based on accepted appointments
        print("6.4 Caregivers earning above average (based on accepted appointments):")
        try:
            results = session.execute(
                text("""
                    SELECT 
                        cg.caregiver_user_id,
                        u.given_name || ' ' || u.surname AS caregiver_name,
                        cg.hourly_rate,
                        (SELECT AVG(cg2.hourly_rate)
                         FROM appointment a2
                         JOIN caregiver cg2 ON a2.caregiver_user_id = cg2.caregiver_user_id
                         WHERE a2.status = 'accepted') AS average_rate
                    FROM appointment a
                    JOIN caregiver cg ON a.caregiver_user_id = cg.caregiver_user_id
                    JOIN users u ON cg.caregiver_user_id = u.user_id
                    WHERE a.status = 'accepted'
                      AND cg.hourly_rate > (
                          SELECT AVG(cg2.hourly_rate)
                          FROM appointment a2
                          JOIN caregiver cg2 ON a2.caregiver_user_id = cg2.caregiver_user_id
                          WHERE a2.status = 'accepted'
                      )
                    GROUP BY cg.caregiver_user_id, u.given_name, u.surname, cg.hourly_rate
                    ORDER BY cg.hourly_rate DESC
                """)
            ).fetchall()
            print_results(results, "Caregivers Earning Above Average")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # ============================================================
        # 7. QUERY WITH DERIVED ATTRIBUTE
        # ============================================================
        print_separator("7. QUERY WITH DERIVED ATTRIBUTE")
        
        print("7. Total cost per caregiver for all accepted appointments:")
        try:
            results = session.execute(
                text("""
                    SELECT 
                        cg.caregiver_user_id,
                        u.given_name || ' ' || u.surname AS caregiver_name,
                        cg.hourly_rate,
                        SUM(a.work_hours) AS total_hours,
                        SUM(cg.hourly_rate * a.work_hours) AS total_cost
                    FROM appointment a
                    JOIN caregiver cg ON a.caregiver_user_id = cg.caregiver_user_id
                    JOIN users u ON cg.caregiver_user_id = u.user_id
                    WHERE a.status = 'accepted'
                    GROUP BY cg.caregiver_user_id, u.given_name, u.surname, cg.hourly_rate
                    ORDER BY total_cost DESC
                """)
            ).fetchall()
            print_results(results, "Total Cost per Caregiver (hourly_rate * work_hours)")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        # ============================================================
        # 8. VIEW OPERATION
        # ============================================================
        print_separator("8. VIEW OPERATION")
        
        print("8. Creating and querying job_applications_view...")
        try:
            # Drop view if it exists
            session.execute(text("DROP VIEW IF EXISTS job_applications_view"))
            session.commit()
            
            # Create view
            session.execute(
                text("""
                    CREATE VIEW job_applications_view AS
                    SELECT 
                        ja.caregiver_user_id,
                        ja.job_id,
                        ja.date_applied,
                        u.given_name || ' ' || u.surname AS applicant_name,
                        j.required_caregiving_type
                    FROM job_application ja
                    JOIN caregiver cg ON ja.caregiver_user_id = cg.caregiver_user_id
                    JOIN users u ON cg.caregiver_user_id = u.user_id
                    JOIN job j ON ja.job_id = j.job_id
                """)
            )
            session.commit()
            print("✓ View created successfully")
            
            # Query the view
            print("\nQuerying job_applications_view:")
            results = session.execute(
                text("SELECT * FROM job_applications_view ORDER BY job_id, caregiver_user_id")
            ).fetchall()
            print_results(results, "Job Applications View")
        except Exception as e:
            session.rollback()
            print(f"✗ Error: {e}")
        
        print_separator("ALL OPERATIONS COMPLETED")
        print("✓ All SQL operations have been executed successfully!")
        
    except Exception as e:
        print(f"\n✗ Fatal Error: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    main()

