# CSCI 341 - Assignment 3 - Part 3
## Online Caregivers Platform - Web Application

This is a Flask web application that provides CRUD (Create, Read, Update, Delete) operations for all database tables in the Caregiver Platform system.

## Features

- Full CRUD operations for all 7 database tables:
  - Users
  - Caregivers
  - Members
  - Addresses
  - Jobs
  - Job Applications
  - Appointments

- Modern, responsive web interface
- Error handling and user feedback
- Database connection using SQLAlchemy

## Prerequisites

- Python 3.7 or higher
- PostgreSQL database (with the caregiver_platform database created)
- All dependencies listed in `requirements.txt`

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Update database connection in `app.py`:
   - Edit the `DATABASE_URL` variable with your PostgreSQL credentials:
   ```python
   DATABASE_URL = 'postgresql://username:password@localhost/caregiver_platform'
   ```

3. Ensure your PostgreSQL database is running and contains the required tables.

## Running the Application

### Local Development

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Production Deployment

#### PythonAnywhere

1. Create a free account at [PythonAnywhere](https://www.pythonanywhere.com/)
2. Upload your project files
3. Create a new web app
4. Set the working directory to your project folder
5. Update the WSGI configuration file to point to `app.py`
6. Update database connection to use your PythonAnywhere database credentials

#### Heroku

1. Install Heroku CLI
2. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Deploy:
   ```bash
   heroku create
   git push heroku main
   heroku addons:create heroku-postgresql:hobby-dev
   ```

#### Amazon EC2 (Educational Tier)

1. Sign up with your university email (@nu.edu.kz)
2. Launch an EC2 instance
3. Install Python, PostgreSQL, and dependencies
4. Configure security groups to allow HTTP/HTTPS traffic
5. Use a process manager like `gunicorn` with `nginx` as reverse proxy

## Project Structure

```
.
├── app.py                      # Main Flask application
├── main.py                     # Part 2: SQL queries script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── templates/                  # HTML templates
    ├── base.html              # Base template
    ├── index.html             # Home page
    ├── users/                 # User templates
    ├── caregivers/           # Caregiver templates
    ├── members/              # Member templates
    ├── addresses/            # Address templates
    ├── jobs/                 # Job templates
    ├── job_applications/     # Job application templates
    └── appointments/         # Appointment templates
```

## Usage

1. Navigate to the home page
2. Select a table from the navigation menu
3. Use the "Create" button to add new records
4. Use "Update" to modify existing records
5. Use "Delete" to remove records (with confirmation)

## Notes

- Foreign key constraints are enforced by the database
- When deleting records, ensure related records are deleted first (e.g., delete job_applications before deleting jobs)
- The application uses the same database connection as Part 2 (`main.py`)

## Troubleshooting

- **Database connection errors**: Verify PostgreSQL is running and credentials are correct
- **Import errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`
- **Port already in use**: Change the port in `app.py` (last line) or stop the process using port 5000

## License

This project is part of CSCI 341 Database Management Systems course assignment.

