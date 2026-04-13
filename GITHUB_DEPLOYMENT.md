# GitHub & Deployment Guide

## Table of Contents
1. [GitHub Setup](#github-setup)
2. [Environment Configuration](#environment-configuration)
3. [Deployment Platforms](#deployment-platforms)
4. [Security Checklist](#security-checklist)
5. [Production Deployment](#production-deployment)

---

## GitHub Setup

### 1. Initialize Git Repository

```bash
# Initialize git (if not already initialized)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: FastAPI authentication application"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/fluffy-octo-waffle.git

# Push to main branch
git branch -M main
git push -u origin main
```

### 2. GitHub Repository Configuration

**Recommended Settings:**

1. **Settings → General**
   - Template repository: Disabled (unless you want it as a template)
   - Push notifications: Enable
   - Automatically delete head branches: Enable

2. **Settings → Branches**
   - Set `main` as default branch
   - Add branch protection rules:
     - Require pull request reviews before merging
     - Dismiss stale pull request approvals
     - Require branches to be up to date before merging

3. **Settings → Secrets and variables → Actions**
   - Add required secrets for CI/CD:
     ```
     SECRET_KEY=your-production-secret-key-here
     DATABASE_URL=your-production-database-url
     ALLOWED_ORIGINS=your-production-domain
     ```

4. **Settings → Deploy keys** (Optional)
   - Add SSH key for automated deployments

### 3. .gitignore Verification

The `.gitignore` file is already configured to exclude:
- Python cache files (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- Environment files (`.env`)
- IDE files (`.vscode/`, `.idea/`)
- Database files (`*.db`, `*.sqlite3`)
- Logs (`logs/`, `*.log`)
- OS-specific files (`.DS_Store`, `Thumbs.db`)

---

## Environment Configuration

### 1. Create `.env` file locally

Copy from `.env.example` and configure for your environment:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
# Database Configuration
DATABASE_URL=sqlite:///./auth.db  # For development
# DATABASE_URL=mysql+pymysql://user:password@host:3306/auth_db  # For MySQL

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=False

# Server
HOST=0.0.0.0
PORT=8000

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,https://yourdomain.com
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database Connection Pool (optional)
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
```

### 2. Generate Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Important:** Use a different SECRET_KEY for production!

### 3. Database Setup

#### SQLite (Default - Development)
```bash
# Database file will be created automatically at ./auth.db
# No additional setup needed
```

#### MySQL (Production Alternative)
```bash
# Install MySQL server and create database
mysql -u root -p
CREATE DATABASE auth_db;
CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON auth_db.* TO 'auth_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Update .env with MySQL connection string
DATABASE_URL=mysql+pymysql://auth_user:your_password@localhost:3306/auth_db
```

---

## Deployment Platforms

### Option 1: Heroku

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Deployment Steps

1. **Install Heroku CLI**
   ```bash
   # Windows
   choco install heroku-cli
   
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set ALLOWED_ORIGINS=https://your-app-name.herokuapp.com
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   heroku config:set DEBUG=False
   ```

5. **Create Procfile** (save as `Procfile` in root)
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT main:app --worker-class uvicorn.workers.UvicornWorker
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

7. **View Logs**
   ```bash
   heroku logs --tail
   ```

---

### Option 2: Railway

#### Prerequisites
- Railway account
- GitHub connected to Railway

#### Deployment Steps

1. **Connect Repository**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Authorize and select your repository

2. **Configure Variables**
   - In Railway dashboard, go to Variables
   - Add all environment variables from `.env.example`

3. **Configure Dockerfile**
   - Railway will auto-detect `Dockerfile`
   - Make sure it's in the root directory (already configured)

4. **Deploy**
   - Railway automatically deploys on push to main
   - View logs in Railway dashboard

#### Custom Domain
- Go to Settings → Custom Domain
- Add your domain (requires DNS configuration)

---

### Option 3: Render

#### Prerequisites
- Render account
- GitHub connected to Render

#### Deployment Steps

1. **Connect Repository**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your repository

2. **Configuration**
   - **Name:** `auth-api` (or your choice)
   - **Region:** Choose closest to users
   - **Branch:** `main`
   - **Runtime:** `Docker`
   - **Build Command:** (leave empty - uses Dockerfile)
   - **Start Command:** (leave empty - uses Dockerfile)

3. **Environment Variables**
   - Add all variables from `.env.example`
   - Use Render's PostgreSQL for production (optional)

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically

#### Auto-Deploy
- Render automatically deploys on push to main (redeploy on every push)

---

### Option 4: Docker Hub + AWS EC2

#### Prerequisites
- Docker Hub account
- AWS account with EC2 instance

#### Deployment Steps

1. **Build Docker Image**
   ```bash
   docker build -t your-dockerhub-username/auth-api:latest .
   ```

2. **Push to Docker Hub**
   ```bash
   docker login
   docker push your-dockerhub-username/auth-api:latest
   ```

3. **Deploy on AWS EC2**
   ```bash
   # SSH into EC2 instance
   ssh -i your-key.pem ec2-user@your-instance-ip
   
   # Install Docker
   sudo yum update -y
   sudo yum install docker -y
   sudo systemctl start docker
   sudo usermod -aG docker ec2-user
   
   # Pull and run container
   docker pull your-dockerhub-username/auth-api:latest
   docker run -d \
     -p 80:8000 \
     -e SECRET_KEY=your-secret-key \
     -e ALLOWED_ORIGINS=your-domain \
     --name auth-api \
     your-dockerhub-username/auth-api:latest
   ```

4. **Configure Nginx Reverse Proxy**
   ```bash
   sudo yum install nginx -y
   sudo systemctl start nginx
   
   # Update /etc/nginx/nginx.conf with the provided nginx.conf
   sudo cp nginx.conf /etc/nginx/nginx.conf
   sudo systemctl reload nginx
   ```

---

### Option 5: DigitalOcean App Platform

#### Deployment Steps

1. **Connect GitHub**
   - Go to https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Select GitHub source
   - Authorize and select repository

2. **Configure**
   - **Name:** `auth-api`
   - **Source:** Docker (auto-detected)
   - **HTTP Port:** 8000

3. **Environment Variables**
   - Add all from `.env.example`

4. **Deploy**
   - Click "Create Resources"
   - DigitalOcean builds and deploys automatically

---

## Security Checklist

Before deploying to production:

- [ ] **Change SECRET_KEY** - Generate new secure key using `secrets.token_urlsafe(32)`
- [ ] **Set DEBUG=False** - Disable debug mode in production
- [ ] **Update ALLOWED_ORIGINS** - Specify your production domain(s)
- [ ] **Update ALLOWED_HOSTS** - List your production hostnames
- [ ] **Use HTTPS** - Enable SSL/TLS certificate (auto-available on most platforms)
- [ ] **Database Backup** - Plan regular database backups
- [ ] **Update Requirements** - Regularly update dependencies: `pip list --outdated`
- [ ] **Security Headers** - Configured in Nginx (nginx.conf)
- [ ] **CORS Configuration** - Only allow trusted origins
- [ ] **Password Hashing** - Verify bcrypt is working without warnings
- [ ] **Log Monitoring** - Set up log aggregation (Sentry, LogRocket, etc.)
- [ ] **Rate Limiting** - Consider adding rate limiting middleware
- [ ] **SSL Certificate** - Install and configure SSL certificate
- [ ] **Environment Variables** - Never commit `.env` file
- [ ] **Database Credentials** - Use strong, unique passwords

---

## Production Deployment

### Best Practices

1. **Always use environment variables**
   ```python
   from dotenv import load_dotenv
   import os
   load_dotenv()
   
   SECRET_KEY = os.getenv("SECRET_KEY")
   DATABASE_URL = os.getenv("DATABASE_URL")
   ```

2. **Monitor Logs**
   ```bash
   # View application logs
   docker logs auth-api
   
   # Follow logs in real-time
   docker logs -f auth-api
   ```

3. **Regular Updates**
   ```bash
   # Check for outdated packages
   pip list --outdated
   
   # Update in requirements.txt and reinstall
   pip install --upgrade package-name
   ```

4. **Database Migrations**
   - Use SQLAlchemy migrations for production changes
   - Test migrations in staging environment first

### Monitoring & Logging

1. **Application Logs**
   - Configured in `main.py` with timestamp and log levels
   - Set `LOG_LEVEL=INFO` for production

2. **Performance Monitoring**
   - Use `GZIPMiddleware` for compression (already enabled)
   - Monitor response times

3. **Error Tracking**
   - Consider Sentry integration for error tracking
   - Monitor failed login attempts

### Backup Strategy

1. **Database Backups**
   ```bash
   # SQLite backup
   cp auth.db auth.db.backup
   
   # MySQL backup
   mysqldump -u user -p auth_db > auth_db.backup.sql
   ```

2. **Automated Backups**
   - Use platform-specific backup features (Heroku, Railway, etc.)
   - Consider off-site backup storage

---

## Troubleshooting

### Common Issues

1. **502 Bad Gateway**
   - Check if application is running: `docker ps`
   - View logs: `docker logs auth-api`
   - Verify port binding: `docker port auth-api`

2. **Connection Refused**
   - Ensure firewall allows traffic on port 8000
   - Check if Nginx is properly configured

3. **Database Connection Error**
   - Verify `DATABASE_URL` in environment variables
   - Check database credentials
   - Ensure database service is running

4. **CORS Issues**
   - Verify frontend domain is in `ALLOWED_ORIGINS`
   - Check browser console for specific error messages

5. **SSL Certificate Issues**
   - Ensure certificate is installed correctly
   - Check certificate expiration date

---

## Next Steps

1. Push code to GitHub
2. Choose deployment platform based on your needs
3. Follow platform-specific deployment steps
4. Monitor application health and logs
5. Set up regular backups
6. Plan for scaling as user base grows

For questions or issues, refer to:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://sqlalchemy.org/)
- [Docker Documentation](https://docs.docker.com/)
- Platform-specific documentation (Heroku, Railway, Render, etc.)
