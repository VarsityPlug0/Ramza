# Setting Up a New Service and Database on Render

## Overview
This guide will help you set up a new Django web service with a PostgreSQL database on Render using the Ramza's Chillas application.

## Prerequisites
1. You have a Render account (https://render.com)
2. You have this Django application code in a GitHub repository
3. You're familiar with basic Git operations

## Step 1: Create a New PostgreSQL Database on Render

1. Log in to your Render dashboard
2. Click "New" → "PostgreSQL"
3. Configure your database:
   - **Name**: Choose a descriptive name (e.g., `ramzas-chillas-db`)
   - **Region**: Choose the region closest to your users
   - **Plan**: Select the free plan or a paid plan based on your needs
4. Click "Create Database"
5. Wait for the database to finish provisioning (this may take a few minutes)

## Step 2: Get Your Database Connection Details

1. Once your database is provisioned, go to the database dashboard
2. Click on the "Connect" tab
3. Note down the following information:
   - **Hostname**: The database host
   - **Port**: Usually 5432
   - **Database**: The database name
   - **Username**: The database user
   - **Password**: Click "Reset password" to get the password
4. Copy the "External Database URL" - it should look like:
   ```
   postgresql://username:password@host:port/database_name
   ```

## Step 3: Update Configuration Files

### Update render.yaml
Replace the placeholder values in [render.yaml](file:///c%3A/Users/money/Bevan%20The%20IT%20GUY/absa/ramzas-chillas/render.yaml):

```yaml
services:
  - type: web
    name: ramzas-chillas  # Choose a unique name for your service
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python start_server.py"
    envVars:
      - key: DATABASE_URL
        value: "postgresql://username:password@host:port/database_name"  # Your actual database URL from Step 2
      - key: SECRET_KEY
        sync: false  # Render will auto-generate a secret key
      - key: WEB_CONCURRENCY
        value: 4
```

### Example render.yaml with real values:
```yaml
services:
  - type: web
    name: ramzas-chillas-production
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python start_server.py"
    envVars:
      - key: DATABASE_URL
        value: "postgresql://ramzas_user:abc123xyz@db.render.com:5432/ramzas_db"
      - key: SECRET_KEY
        sync: false
      - key: WEB_CONCURRENCY
        value: 4
```

## Step 4: Deploy Your Web Service

1. Commit your changes to GitHub:
   ```bash
   git add .
   git commit -m "Configure for new Render service and database"
   git push origin master
   ```

2. Go to Render dashboard
3. Click "New" → "Web Service"
4. Connect your GitHub repository that contains this Django application
5. Ensure the branch is set to master (or main)
6. Render should automatically detect and use your [render.yaml](file:///c%3A/Users/money/Bevan%20The%20IT%20GUY/absa/ramzas-chillas/render.yaml) configuration
7. Click "Create Web Service"

## Step 5: Monitor Deployment

1. The deployment process will start automatically
2. Watch the build logs in the Render dashboard
3. The process includes:
   - Cloning your repository
   - Running the build command (`pip install -r requirements.txt`)
   - Running the start command (`python start_server.py`)

## Step 6: Verify Successful Deployment

Look for these messages in the deployment logs:

```
=== START SERVER SCRIPT ===
Setting up Django...
Django setup completed successfully
Running Django migrations...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, orders, restaurant, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  # ... more migrations ...
Migrations completed successfully
Creating superuser if needed...
Superuser created successfully
Starting Gunicorn server...
[YYYY-MM-DD HH:MM:SS +0000] [1] [INFO] Starting gunicorn 23.0.0
```

## Step 7: Access Your Application

1. Once deployment is complete, Render will provide a URL for your application
2. It will look like: `https://your-service-name.onrender.com`
3. Visit this URL to see your application running

## Step 8: Access Admin Panel

1. Go to `https://your-app-url.onrender.com/admin/`
2. Login with the default credentials:
   - Username: admin
   - Password: admin123
3. You can change these credentials after logging in

## Troubleshooting Common Issues

### Database Connection Issues
If you see errors like "could not connect to server", check:
1. Database URL in [render.yaml](file:///c%3A/Users/money/Bevan%20The%20IT%20GUY/absa/ramzas-chillas/render.yaml) is correct
2. Database is finished provisioning
3. Database credentials are correct

### Migration Errors
If migrations fail:
1. Check the database connection
2. Verify that all migration files are in your repository
3. Look for specific error messages in the logs

### Application Startup Issues
If the application doesn't start:
1. Check that the start command in [render.yaml](file:///c%3A/Users/money/Bevan%20The%20IT%20GUY/absa/ramzas-chillas/render.yaml) is correct
2. Verify dependencies in [requirements.txt](file:///c%3A/Users/money/Bevan%20The%20IT%20GUY/absa/ramzas-chillas/requirements.txt) are up to date
3. Check the logs for specific error messages

## Environment Variables Explained

- `DATABASE_URL`: PostgreSQL connection string provided by Render
- `SECRET_KEY`: Django secret key (auto-generated by Render)
- `WEB_CONCURRENCY`: Number of Gunicorn worker processes (set to 4 for optimal performance)
- `PORT`: Port for the application (provided automatically by Render)

## How the Startup Process Works

The [start_server.py](file:///c%3A/Users/money/Bevan%20The%20IT%20GUY/absa/ramzas-chillas/start_server.py) script handles the complete startup process:

1. **Django Setup**: Configures the Django environment
2. **Database Migrations**: Automatically runs `python manage.py migrate --noinput`
3. **Superuser Creation**: Creates a default admin user if one doesn't exist
4. **Application Start**: Launches Gunicorn to serve the Django application

This ensures your application is always properly configured and ready to serve requests.

## Security Considerations

1. The default admin credentials should be changed after first login
2. Consider adding additional environment variables for sensitive configuration
3. Review the [requirements.txt](file:///c%3A/Users/money/Bevan%20The%20IT%20GUY/absa/ramzas-chillas/requirements.txt) for any outdated packages
4. Ensure your GitHub repository has appropriate access controls

## Next Steps

1. Log in to the admin panel and customize your site content
2. Test all functionality to ensure everything works correctly
3. Set up custom domain if needed
4. Configure SSL (Render provides this automatically)
5. Monitor application performance and logs