"""
CSCI 341 - Database Management Systems
Assignment 3 - Part 3
Online Caregivers Platform - Web Application (Flask)

Flask web application with CRUD operations for all database tables.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Database connection
# Use environment variable for production, fallback to local for development
import os
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:123456@localhost/caregiver_platform')
# Render.com provides DATABASE_URL with postgres://, need to convert to postgresql://
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """Create a new database session"""
    return SessionLocal()


# ============================================================
# USERS TABLE CRUD
# ============================================================

@app.route('/')
def index():
    """Home page - list all tables"""
    return render_template('index.html')


@app.route('/users')
def users_list():
    """List all users"""
    session = get_session()
    try:
        users = session.execute(
            text("SELECT * FROM users ORDER BY user_id")
        ).fetchall()
        return render_template('users/list.html', users=users, page_title='Users')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('users/list.html', users=[])
    finally:
        session.close()


@app.route('/users/create', methods=['GET', 'POST'])
def users_create():
    """Create a new user"""
    if request.method == 'POST':
        session = get_session()
        try:
            session.execute(
                text("""
                    INSERT INTO users (email, given_name, surname, city, phone_number, 
                                     profile_description, password)
                    VALUES (:email, :given_name, :surname, :city, :phone_number, 
                            :profile_description, :password)
                """),
                {
                    'email': request.form['email'],
                    'given_name': request.form['given_name'],
                    'surname': request.form['surname'],
                    'city': request.form.get('city') or None,
                    'phone_number': request.form.get('phone_number') or None,
                    'profile_description': request.form.get('profile_description') or None,
                    'password': request.form['password']
                }
            )
            session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('users_list'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating user: {str(e)}', 'error')
        finally:
            session.close()
    return render_template('users/create.html')


@app.route('/users/<int:user_id>/update', methods=['GET', 'POST'])
def users_update(user_id):
    """Update a user"""
    session = get_session()
    try:
        if request.method == 'POST':
            session.execute(
                text("""
                    UPDATE users 
                    SET email = :email, given_name = :given_name, surname = :surname,
                        city = :city, phone_number = :phone_number, 
                        profile_description = :profile_description, password = :password
                    WHERE user_id = :user_id
                """),
                {
                    'user_id': user_id,
                    'email': request.form['email'],
                    'given_name': request.form['given_name'],
                    'surname': request.form['surname'],
                    'city': request.form.get('city') or None,
                    'phone_number': request.form.get('phone_number') or None,
                    'profile_description': request.form.get('profile_description') or None,
                    'password': request.form['password']
                }
            )
            session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('users_list'))
        
        # GET request - fetch user data
        user = session.execute(
            text("SELECT * FROM users WHERE user_id = :user_id"),
            {'user_id': user_id}
        ).fetchone()
        
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('users_list'))
        
        return render_template('users/update.html', user=user)
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('users_list'))
    finally:
        session.close()


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def users_delete(user_id):
    """Delete a user"""
    session = get_session()
    try:
        session.execute(
            text("DELETE FROM users WHERE user_id = :user_id"),
            {'user_id': user_id}
        )
        session.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('users_list'))


# ============================================================
# CAREGIVER TABLE CRUD
# ============================================================

@app.route('/caregivers')
def caregivers_list():
    """List all caregivers"""
    session = get_session()
    try:
        caregivers = session.execute(
            text("""
                SELECT c.*, u.given_name, u.surname, u.email, u.city, u.phone_number
                FROM caregiver c
                JOIN users u ON c.caregiver_user_id = u.user_id
                ORDER BY c.caregiver_user_id
            """)
        ).fetchall()
        return render_template('caregivers/list.html', caregivers=caregivers)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('caregivers/list.html', caregivers=[])
    finally:
        session.close()


@app.route('/caregivers/create', methods=['GET', 'POST'])
def caregivers_create():
    """Create a new caregiver"""
    session = get_session()
    if request.method == 'POST':
        try:
            session.execute(
                text("""
                    INSERT INTO caregiver (caregiver_user_id, photo, gender, 
                                          caregiving_type, hourly_rate)
                    VALUES (:caregiver_user_id, :photo, :gender, 
                            :caregiving_type, :hourly_rate)
                """),
                {
                    'caregiver_user_id': int(request.form['caregiver_user_id']),
                    'photo': request.form.get('photo') or None,
                    'gender': request.form.get('gender') or None,
                    'caregiving_type': request.form['caregiving_type'],
                    'hourly_rate': float(request.form['hourly_rate'])
                }
            )
            session.commit()
            flash('Caregiver created successfully!', 'success')
            return redirect(url_for('caregivers_list'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating caregiver: {str(e)}', 'error')
        finally:
            session.close()
    
    # GET request - fetch available users
    try:
        users = session.execute(
            text("SELECT user_id, given_name, surname, email FROM users ORDER BY user_id")
        ).fetchall()
        return render_template('caregivers/create.html', users=users)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('caregivers/create.html', users=[])
    finally:
        session.close()


@app.route('/caregivers/<int:caregiver_user_id>/update', methods=['GET', 'POST'])
def caregivers_update(caregiver_user_id):
    """Update a caregiver"""
    session = get_session()
    try:
        if request.method == 'POST':
            session.execute(
                text("""
                    UPDATE caregiver 
                    SET photo = :photo, gender = :gender, 
                        caregiving_type = :caregiving_type, hourly_rate = :hourly_rate
                    WHERE caregiver_user_id = :caregiver_user_id
                """),
                {
                    'caregiver_user_id': caregiver_user_id,
                    'photo': request.form.get('photo') or None,
                    'gender': request.form.get('gender') or None,
                    'caregiving_type': request.form['caregiving_type'],
                    'hourly_rate': float(request.form['hourly_rate'])
                }
            )
            session.commit()
            flash('Caregiver updated successfully!', 'success')
            return redirect(url_for('caregivers_list'))
        
        # GET request
        caregiver = session.execute(
            text("""
                SELECT c.*, u.given_name, u.surname 
                FROM caregiver c
                JOIN users u ON c.caregiver_user_id = u.user_id
                WHERE c.caregiver_user_id = :caregiver_user_id
            """),
            {'caregiver_user_id': caregiver_user_id}
        ).fetchone()
        
        if not caregiver:
            flash('Caregiver not found!', 'error')
            return redirect(url_for('caregivers_list'))
        
        return render_template('caregivers/update.html', caregiver=caregiver)
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('caregivers_list'))
    finally:
        session.close()


@app.route('/caregivers/<int:caregiver_user_id>/delete', methods=['POST'])
def caregivers_delete(caregiver_user_id):
    """Delete a caregiver"""
    session = get_session()
    try:
        session.execute(
            text("DELETE FROM caregiver WHERE caregiver_user_id = :caregiver_user_id"),
            {'caregiver_user_id': caregiver_user_id}
        )
        session.commit()
        flash('Caregiver deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting caregiver: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('caregivers_list'))


# ============================================================
# MEMBER TABLE CRUD
# ============================================================

@app.route('/members')
def members_list():
    """List all members"""
    session = get_session()
    try:
        members = session.execute(
            text("""
                SELECT m.*, u.given_name, u.surname, u.email, u.city, u.phone_number
                FROM member m
                JOIN users u ON m.member_user_id = u.user_id
                ORDER BY m.member_user_id
            """)
        ).fetchall()
        return render_template('members/list.html', members=members)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('members/list.html', members=[])
    finally:
        session.close()


@app.route('/members/create', methods=['GET', 'POST'])
def members_create():
    """Create a new member"""
    session = get_session()
    if request.method == 'POST':
        try:
            session.execute(
                text("""
                    INSERT INTO member (member_user_id, house_rules, dependent_description)
                    VALUES (:member_user_id, :house_rules, :dependent_description)
                """),
                {
                    'member_user_id': int(request.form['member_user_id']),
                    'house_rules': request.form.get('house_rules') or None,
                    'dependent_description': request.form.get('dependent_description') or None
                }
            )
            session.commit()
            flash('Member created successfully!', 'success')
            return redirect(url_for('members_list'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating member: {str(e)}', 'error')
        finally:
            session.close()
    
    # GET request
    try:
        users = session.execute(
            text("SELECT user_id, given_name, surname, email FROM users ORDER BY user_id")
        ).fetchall()
        return render_template('members/create.html', users=users)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('members/create.html', users=[])
    finally:
        session.close()


@app.route('/members/<int:member_user_id>/update', methods=['GET', 'POST'])
def members_update(member_user_id):
    """Update a member"""
    session = get_session()
    try:
        if request.method == 'POST':
            session.execute(
                text("""
                    UPDATE member 
                    SET house_rules = :house_rules, dependent_description = :dependent_description
                    WHERE member_user_id = :member_user_id
                """),
                {
                    'member_user_id': member_user_id,
                    'house_rules': request.form.get('house_rules') or None,
                    'dependent_description': request.form.get('dependent_description') or None
                }
            )
            session.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('members_list'))
        
        # GET request
        member = session.execute(
            text("""
                SELECT m.*, u.given_name, u.surname 
                FROM member m
                JOIN users u ON m.member_user_id = u.user_id
                WHERE m.member_user_id = :member_user_id
            """),
            {'member_user_id': member_user_id}
        ).fetchone()
        
        if not member:
            flash('Member not found!', 'error')
            return redirect(url_for('members_list'))
        
        return render_template('members/update.html', member=member)
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('members_list'))
    finally:
        session.close()


@app.route('/members/<int:member_user_id>/delete', methods=['POST'])
def members_delete(member_user_id):
    """Delete a member"""
    session = get_session()
    try:
        session.execute(
            text("DELETE FROM member WHERE member_user_id = :member_user_id"),
            {'member_user_id': member_user_id}
        )
        session.commit()
        flash('Member deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting member: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('members_list'))


# ============================================================
# ADDRESS TABLE CRUD
# ============================================================

@app.route('/addresses')
def addresses_list():
    """List all addresses"""
    session = get_session()
    try:
        addresses = session.execute(
            text("""
                SELECT a.*, u.given_name, u.surname
                FROM address a
                JOIN member m ON a.member_user_id = m.member_user_id
                JOIN users u ON m.member_user_id = u.user_id
                ORDER BY a.member_user_id
            """)
        ).fetchall()
        return render_template('addresses/list.html', addresses=addresses)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('addresses/list.html', addresses=[])
    finally:
        session.close()


@app.route('/addresses/create', methods=['GET', 'POST'])
def addresses_create():
    """Create a new address"""
    session = get_session()
    if request.method == 'POST':
        try:
            session.execute(
                text("""
                    INSERT INTO address (member_user_id, house_number, street, town)
                    VALUES (:member_user_id, :house_number, :street, :town)
                """),
                {
                    'member_user_id': int(request.form['member_user_id']),
                    'house_number': request.form.get('house_number') or None,
                    'street': request.form.get('street') or None,
                    'town': request.form.get('town') or None
                }
            )
            session.commit()
            flash('Address created successfully!', 'success')
            return redirect(url_for('addresses_list'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating address: {str(e)}', 'error')
        finally:
            session.close()
    
    # GET request
    try:
        members = session.execute(
            text("""
                SELECT m.member_user_id, u.given_name, u.surname, u.email
                FROM member m
                JOIN users u ON m.member_user_id = u.user_id
                ORDER BY m.member_user_id
            """)
        ).fetchall()
        return render_template('addresses/create.html', members=members)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('addresses/create.html', members=[])
    finally:
        session.close()


@app.route('/addresses/<int:member_user_id>/update', methods=['GET', 'POST'])
def addresses_update(member_user_id):
    """Update an address"""
    session = get_session()
    try:
        if request.method == 'POST':
            session.execute(
                text("""
                    UPDATE address 
                    SET house_number = :house_number, street = :street, town = :town
                    WHERE member_user_id = :member_user_id
                """),
                {
                    'member_user_id': member_user_id,
                    'house_number': request.form.get('house_number') or None,
                    'street': request.form.get('street') or None,
                    'town': request.form.get('town') or None
                }
            )
            session.commit()
            flash('Address updated successfully!', 'success')
            return redirect(url_for('addresses_list'))
        
        # GET request
        address = session.execute(
            text("""
                SELECT a.*, u.given_name, u.surname 
                FROM address a
                JOIN member m ON a.member_user_id = m.member_user_id
                JOIN users u ON m.member_user_id = u.user_id
                WHERE a.member_user_id = :member_user_id
            """),
            {'member_user_id': member_user_id}
        ).fetchone()
        
        if not address:
            flash('Address not found!', 'error')
            return redirect(url_for('addresses_list'))
        
        return render_template('addresses/update.html', address=address)
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('addresses_list'))
    finally:
        session.close()


@app.route('/addresses/<int:member_user_id>/delete', methods=['POST'])
def addresses_delete(member_user_id):
    """Delete an address"""
    session = get_session()
    try:
        session.execute(
            text("DELETE FROM address WHERE member_user_id = :member_user_id"),
            {'member_user_id': member_user_id}
        )
        session.commit()
        flash('Address deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting address: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('addresses_list'))


# ============================================================
# JOB TABLE CRUD
# ============================================================

@app.route('/jobs')
def jobs_list():
    """List all jobs"""
    session = get_session()
    try:
        jobs = session.execute(
            text("""
                SELECT j.*, u.given_name, u.surname, u.email
                FROM job j
                JOIN member m ON j.member_user_id = m.member_user_id
                JOIN users u ON m.member_user_id = u.user_id
                ORDER BY j.job_id
            """)
        ).fetchall()
        return render_template('jobs/list.html', jobs=jobs)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('jobs/list.html', jobs=[])
    finally:
        session.close()


@app.route('/jobs/create', methods=['GET', 'POST'])
def jobs_create():
    """Create a new job"""
    session = get_session()
    if request.method == 'POST':
        try:
            session.execute(
                text("""
                    INSERT INTO job (member_user_id, required_caregiving_type, 
                                   other_requirements, date_posted)
                    VALUES (:member_user_id, :required_caregiving_type, 
                            :other_requirements, :date_posted)
                """),
                {
                    'member_user_id': int(request.form['member_user_id']),
                    'required_caregiving_type': request.form['required_caregiving_type'],
                    'other_requirements': request.form.get('other_requirements') or None,
                    'date_posted': request.form.get('date_posted') or datetime.now().date()
                }
            )
            session.commit()
            flash('Job created successfully!', 'success')
            return redirect(url_for('jobs_list'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating job: {str(e)}', 'error')
        finally:
            session.close()
    
    # GET request
    try:
        members = session.execute(
            text("""
                SELECT m.member_user_id, u.given_name, u.surname, u.email
                FROM member m
                JOIN users u ON m.member_user_id = u.user_id
                ORDER BY m.member_user_id
            """)
        ).fetchall()
        return render_template('jobs/create.html', members=members, today=date.today())
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('jobs/create.html', members=[])
    finally:
        session.close()


@app.route('/jobs/<int:job_id>/update', methods=['GET', 'POST'])
def jobs_update(job_id):
    """Update a job"""
    session = get_session()
    try:
        if request.method == 'POST':
            session.execute(
                text("""
                    UPDATE job 
                    SET required_caregiving_type = :required_caregiving_type,
                        other_requirements = :other_requirements, 
                        date_posted = :date_posted
                    WHERE job_id = :job_id
                """),
                {
                    'job_id': job_id,
                    'required_caregiving_type': request.form['required_caregiving_type'],
                    'other_requirements': request.form.get('other_requirements') or None,
                    'date_posted': request.form.get('date_posted') or datetime.now().date()
                }
            )
            session.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('jobs_list'))
        
        # GET request
        job = session.execute(
            text("""
                SELECT j.*, u.given_name, u.surname 
                FROM job j
                JOIN member m ON j.member_user_id = m.member_user_id
                JOIN users u ON m.member_user_id = u.user_id
                WHERE j.job_id = :job_id
            """),
            {'job_id': job_id}
        ).fetchone()
        
        if not job:
            flash('Job not found!', 'error')
            return redirect(url_for('jobs_list'))
        
        return render_template('jobs/update.html', job=job)
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('jobs_list'))
    finally:
        session.close()


@app.route('/jobs/<int:job_id>/delete', methods=['POST'])
def jobs_delete(job_id):
    """Delete a job"""
    session = get_session()
    try:
        # First delete job applications
        session.execute(
            text("DELETE FROM job_application WHERE job_id = :job_id"),
            {'job_id': job_id}
        )
        # Then delete the job
        session.execute(
            text("DELETE FROM job WHERE job_id = :job_id"),
            {'job_id': job_id}
        )
        session.commit()
        flash('Job deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting job: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('jobs_list'))


# ============================================================
# JOB_APPLICATION TABLE CRUD
# ============================================================

@app.route('/job_applications')
def job_applications_list():
    """List all job applications"""
    session = get_session()
    try:
        applications = session.execute(
            text("""
                SELECT ja.*, 
                       cg_u.given_name || ' ' || cg_u.surname AS caregiver_name,
                       m_u.given_name || ' ' || m_u.surname AS member_name,
                       j.required_caregiving_type
                FROM job_application ja
                JOIN caregiver cg ON ja.caregiver_user_id = cg.caregiver_user_id
                JOIN users cg_u ON cg.caregiver_user_id = cg_u.user_id
                JOIN job j ON ja.job_id = j.job_id
                JOIN member m ON j.member_user_id = m.member_user_id
                JOIN users m_u ON m.member_user_id = m_u.user_id
                ORDER BY ja.job_id, ja.caregiver_user_id
            """)
        ).fetchall()
        return render_template('job_applications/list.html', applications=applications)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('job_applications/list.html', applications=[])
    finally:
        session.close()


@app.route('/job_applications/create', methods=['GET', 'POST'])
def job_applications_create():
    """Create a new job application"""
    session = get_session()
    if request.method == 'POST':
        try:
            session.execute(
                text("""
                    INSERT INTO job_application (caregiver_user_id, job_id, date_applied)
                    VALUES (:caregiver_user_id, :job_id, :date_applied)
                """),
                {
                    'caregiver_user_id': int(request.form['caregiver_user_id']),
                    'job_id': int(request.form['job_id']),
                    'date_applied': request.form.get('date_applied') or datetime.now().date()
                }
            )
            session.commit()
            flash('Job application created successfully!', 'success')
            return redirect(url_for('job_applications_list'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating job application: {str(e)}', 'error')
        finally:
            session.close()
    
    # GET request
    try:
        caregivers = session.execute(
            text("""
                SELECT cg.caregiver_user_id, u.given_name, u.surname, u.email
                FROM caregiver cg
                JOIN users u ON cg.caregiver_user_id = u.user_id
                ORDER BY cg.caregiver_user_id
            """)
        ).fetchall()
        jobs = session.execute(
            text("SELECT job_id, required_caregiving_type, date_posted FROM job ORDER BY job_id")
        ).fetchall()
        return render_template('job_applications/create.html', 
                             caregivers=caregivers, jobs=jobs, today=date.today())
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('job_applications/create.html', 
                             caregivers=[], jobs=[])
    finally:
        session.close()


@app.route('/job_applications/delete', methods=['POST'])
def job_applications_delete():
    """Delete a job application"""
    session = get_session()
    try:
        caregiver_user_id = int(request.form['caregiver_user_id'])
        job_id = int(request.form['job_id'])
        session.execute(
            text("""
                DELETE FROM job_application 
                WHERE caregiver_user_id = :caregiver_user_id AND job_id = :job_id
            """),
            {'caregiver_user_id': caregiver_user_id, 'job_id': job_id}
        )
        session.commit()
        flash('Job application deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting job application: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('job_applications_list'))


# ============================================================
# APPOINTMENT TABLE CRUD
# ============================================================

@app.route('/appointments')
def appointments_list():
    """List all appointments"""
    session = get_session()
    try:
        appointments = session.execute(
            text("""
                SELECT a.*, 
                       cg_u.given_name || ' ' || cg_u.surname AS caregiver_name,
                       m_u.given_name || ' ' || m_u.surname AS member_name
                FROM appointment a
                JOIN caregiver cg ON a.caregiver_user_id = cg.caregiver_user_id
                JOIN users cg_u ON cg.caregiver_user_id = cg_u.user_id
                JOIN member m ON a.member_user_id = m.member_user_id
                JOIN users m_u ON m.member_user_id = m_u.user_id
                ORDER BY a.appointment_date DESC, a.appointment_time
            """)
        ).fetchall()
        return render_template('appointments/list.html', appointments=appointments)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('appointments/list.html', appointments=[])
    finally:
        session.close()


@app.route('/appointments/create', methods=['GET', 'POST'])
def appointments_create():
    """Create a new appointment"""
    session = get_session()
    if request.method == 'POST':
        try:
            session.execute(
                text("""
                    INSERT INTO appointment (caregiver_user_id, member_user_id, 
                                          appointment_date, appointment_time, 
                                          work_hours, status)
                    VALUES (:caregiver_user_id, :member_user_id, :appointment_date,
                            :appointment_time, :work_hours, :status)
                """),
                {
                    'caregiver_user_id': int(request.form['caregiver_user_id']),
                    'member_user_id': int(request.form['member_user_id']),
                    'appointment_date': request.form['appointment_date'],
                    'appointment_time': request.form['appointment_time'],
                    'work_hours': float(request.form['work_hours']),
                    'status': request.form['status']
                }
            )
            session.commit()
            flash('Appointment created successfully!', 'success')
            return redirect(url_for('appointments_list'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating appointment: {str(e)}', 'error')
        finally:
            session.close()
    
    # GET request
    try:
        caregivers = session.execute(
            text("""
                SELECT cg.caregiver_user_id, u.given_name, u.surname, u.email
                FROM caregiver cg
                JOIN users u ON cg.caregiver_user_id = u.user_id
                ORDER BY cg.caregiver_user_id
            """)
        ).fetchall()
        members = session.execute(
            text("""
                SELECT m.member_user_id, u.given_name, u.surname, u.email
                FROM member m
                JOIN users u ON m.member_user_id = u.user_id
                ORDER BY m.member_user_id
            """)
        ).fetchall()
        return render_template('appointments/create.html', 
                             caregivers=caregivers, members=members)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('appointments/create.html', 
                             caregivers=[], members=[])
    finally:
        session.close()


@app.route('/appointments/<int:appointment_id>/update', methods=['GET', 'POST'])
def appointments_update(appointment_id):
    """Update an appointment"""
    session = get_session()
    try:
        if request.method == 'POST':
            session.execute(
                text("""
                    UPDATE appointment 
                    SET appointment_date = :appointment_date,
                        appointment_time = :appointment_time,
                        work_hours = :work_hours, status = :status
                    WHERE appointment_id = :appointment_id
                """),
                {
                    'appointment_id': appointment_id,
                    'appointment_date': request.form['appointment_date'],
                    'appointment_time': request.form['appointment_time'],
                    'work_hours': float(request.form['work_hours']),
                    'status': request.form['status']
                }
            )
            session.commit()
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('appointments_list'))
        
        # GET request
        appointment = session.execute(
            text("""
                SELECT a.*, 
                       cg_u.given_name || ' ' || cg_u.surname AS caregiver_name,
                       m_u.given_name || ' ' || m_u.surname AS member_name
                FROM appointment a
                JOIN caregiver cg ON a.caregiver_user_id = cg.caregiver_user_id
                JOIN users cg_u ON cg.caregiver_user_id = cg_u.user_id
                JOIN member m ON a.member_user_id = m.member_user_id
                JOIN users m_u ON m.member_user_id = m_u.user_id
                WHERE a.appointment_id = :appointment_id
            """),
            {'appointment_id': appointment_id}
        ).fetchone()
        
        if not appointment:
            flash('Appointment not found!', 'error')
            return redirect(url_for('appointments_list'))
        
        return render_template('appointments/update.html', appointment=appointment)
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('appointments_list'))
    finally:
        session.close()


@app.route('/appointments/<int:appointment_id>/delete', methods=['POST'])
def appointments_delete(appointment_id):
    """Delete an appointment"""
    session = get_session()
    try:
        session.execute(
            text("DELETE FROM appointment WHERE appointment_id = :appointment_id"),
            {'appointment_id': appointment_id}
        )
        session.commit()
        flash('Appointment deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting appointment: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('appointments_list'))


if __name__ == '__main__':
    # Only run in debug mode if not in production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

