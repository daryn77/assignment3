# Deployment Guide for Render.com

This guide will help you deploy the Caregiver Platform application to Render.com.

## Prerequisites

1. A GitHub account with the repository pushed (already done)
2. A Render.com account (sign up at https://render.com)
3. A PostgreSQL database (can be created on Render.com)

## Step 1: Create PostgreSQL Database on Render.com

1. Log in to your Render.com dashboard
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `caregiver-platform-db` (or any name you prefer)
   - **Database**: `caregiver_platform`
   - **User**: Auto-generated
   - **Region**: Choose closest to you
   - **Plan**: Free tier is fine for testing
4. Click "Create Database"
5. **Important**: Copy the **Internal Database URL** - you'll need this later

## Step 2: Import Your Database Schema

1. In your Render PostgreSQL dashboard, go to "Connect" tab
2. Use the "psql" connection string or connect via pgAdmin
3. Import your database schema:
   - Export your local database using: `pg_dump -h localhost -U postgres caregiver_platform > database.sql`
   - Or use the SQL scripts you created in Part 1
   - Import the schema into your Render PostgreSQL database

## Step 3: Create Web Service on Render.com

1. In Render dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository:
   - Select "Public Git repository"
   - Enter: `https://github.com/daryn77/assignment3.git`
   - Or connect your GitHub account and select the repository
3. Configure the service:
   - **Name**: `caregiver-platform` (or any name)
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`

## Step 4: Configure Environment Variables

In your Web Service settings, go to "Environment" tab and add:

1. **DATABASE_URL**: 
   - Use the **Internal Database URL** from your PostgreSQL service
   - Format: `postgresql://user:password@host:port/database`
   - Render automatically converts `postgres://` to `postgresql://` in the code

2. **SECRET_KEY**: 
   - Generate a random secret key for Flask sessions
   - You can use: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Or use any long random string

3. **FLASK_ENV**: 
   - Set to `production` (this disables debug mode)

## Step 5: Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start the application using gunicorn
3. Wait for the build to complete (usually 2-5 minutes)
4. Your app will be available at: `https://your-app-name.onrender.com`

## Step 6: Verify Deployment

1. Visit your app URL
2. Test the CRUD operations
3. Check logs in Render dashboard if there are any issues

## Troubleshooting

### Database Connection Issues
- Ensure `DATABASE_URL` is set correctly
- Use the **Internal Database URL** (not external) if database is on Render
- Check that database is in the same region as web service

### Build Failures
- Check build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

### Application Errors
- Check application logs in Render dashboard
- Verify environment variables are set correctly
- Ensure database schema is imported

## Files Created for Deployment

- `wsgi.py` - WSGI entry point for gunicorn
- `Procfile` - Process file for Render.com
- `render.yaml` - Optional Render configuration file
- `.gitignore` - Git ignore file
- `requirements.txt` - Updated with gunicorn

## Notes

- Render.com free tier spins down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- For production, consider upgrading to a paid plan
- Database backups are recommended for production use

## Support

If you encounter issues:
1. Check Render.com documentation: https://render.com/docs
2. Review application logs in Render dashboard
3. Verify all environment variables are set correctly

