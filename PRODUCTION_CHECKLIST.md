# Production Deployment Checklist

## Pre-Deployment (Before Pushing to GitHub)

### 1. Security
- [ ] Change `SECRET_KEY` to a unique, strong value
  - Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Set `DEBUG=False` in production environment
- [ ] Verify no hardcoded credentials in code
- [ ] Review all API endpoints for authentication requirements
- [ ] Test JWT token expiration (should be 30 minutes)
- [ ] Verify password hashing uses bcrypt (passlib)
- [ ] No `.env` file should be committed (already in `.gitignore`)

### 2. Code Quality
- [ ] Run syntax check: `python -m py_compile $(find . -name '*.py')`
- [ ] All imports are used (check for unused imports)
- [ ] Logging configured correctly with different levels
- [ ] Error handling in place for all critical operations
- [ ] Database migrations tested
- [ ] No print statements in production code (use logging instead)

### 3. Dependencies
- [ ] All required packages in `requirements.txt`
- [ ] No development-only dependencies in requirements.txt
- [ ] Versions pinned for consistency
- [ ] No deprecated packages
- [ ] Run `pip freeze > requirements.txt` to verify

### 4. Database
- [ ] Database tables created successfully
- [ ] Default admin user created (if needed)
- [ ] Database backup migration plan established
- [ ] Connection pooling configured (if using MySQL)
- [ ] Indexes created on frequently queried columns

### 5. Static Files & Frontend
- [ ] All CSS files minified (optional but recommended)
- [ ] All JavaScript files minified (optional but recommended)
- [ ] Images optimized for web
- [ ] No console errors in browser (F12 developer tools)
- [ ] Frontend responsive design tested on mobile
- [ ] All external CDNs (FontAwesome, Bootstrap) accessible

### 6. Configuration Files
- [ ] `.env.example` has all required variables with descriptions
- [ ] `.gitignore` includes all sensitive files
- [ ] `docker-compose.yml` updated for production
- [ ] `Dockerfile` uses multi-stage build
- [ ] `nginx.conf` configured correctly
- [ ] `Procfile` ready for Heroku (if deploying to Heroku)

### 7. Documentation
- [ ] `README.md` has clear setup instructions
- [ ] `GITHUB_DEPLOYMENT.md` complete with all platforms
- [ ] API documentation accessible at `/docs` (FastAPI auto-generates)
- [ ] Comments in complex code sections

### 8. Testing
- [ ] Authentication flow tested (register → login → access protected route)
- [ ] CORS working correctly for frontend
- [ ] Error responses formatted consistently
- [ ] Server health check endpoint working (`/health`)
- [ ] All static files loading with correct MIME types

---

## GitHub Repository Setup

- [ ] Repository created on GitHub
- [ ] All files pushed to `main` branch
- [ ] Sensitive information not in repository
- [ ] `.gitignore` verified (no `.env`, `__pycache__`, `.db` files)
- [ ] Repository description added
- [ ] Repository topics added (fastapi, authentication, webapi, etc.)
- [ ] Branch protection rules configured (if organization/team project)

---

## Platform-Specific Pre-Deployment

### For Heroku
- [ ] `Procfile` in root directory
- [ ] `requirements.txt` includes `gunicorn` (if not using Procfile with uvicorn)
- [ ] `runtime.txt` created with Python version: `python-3.12.1`
- [ ] Additional buildpacks added if needed

### For Railway
- [ ] `Dockerfile` present and tested locally
- [ ] Environment variables configured in Railway dashboard
- [ ] Health check endpoint accessible
- [ ] Deployment logs reviewed

### For Render
- [ ] `Dockerfile` present and working
- [ ] Build and start commands cleared (uses Dockerfile)
- [ ] Environment variables set in dashboard
- [ ] Custom domain configured (optional)

### For Docker Hub + AWS
- [ ] Docker image builds successfully: `docker build -t app:latest .`
- [ ] Docker image runs locally: `docker run -p 8000:8000 app:latest`
- [ ] AWS EC2 instance running with appropriate security groups
- [ ] Nginx reverse proxy configured
- [ ] SSL certificate installed (with Let's Encrypt)

---

## Deployment Day

### 1. Before Going Live
- [ ] Full backup of current database (if migrating from existing)
- [ ] Team notified of deployment time
- [ ] Rollback plan documented
- [ ] Monitoring/alerting configured
- [ ] Health check set up (platform-specific)

### 2. During Deployment
- [ ] Push code to GitHub
- [ ] Platform automatically detects and deploys (if auto-deploy configured)
- [ ] Monitor build logs for errors
- [ ] Wait for health check to pass
- [ ] Initial smoke tests performed

### 3. After Deployment
- [ ] Access application at production URL
- [ ] Test login functionality (register → login → dashboard)
- [ ] Check logs for errors: `docker logs -f` or platform logs
- [ ] Verify SSL certificate shows no warnings
- [ ] Test from different browsers/devices
- [ ] Monitor error tracking (if configured)
- [ ] Check response times/performance
- [ ] Database connection verified
- [ ] Static assets loading correctly

---

## Post-Deployment Monitoring

### Daily Checks
- [ ] Application error logs reviewed
- [ ] Failed login attempts monitored
- [ ] Response time tracking
- [ ] Database storage usage checked

### Weekly Checks
- [ ] Dependency security updates reviewed
- [ ] SSL certificate expiration monitored
- [ ] Database backup verified
- [ ] Disk space availability checked

### Monthly Tasks
- [ ] Update dependencies: `pip list --outdated`
- [ ] Review and clean up logs
- [ ] Database optimization/maintenance
- [ ] Security audit of new vulnerabilities

---

## Environment Variables Checklist

### Required Variables (Production)
```
✓ DATABASE_URL=actual-production-database-url
✓ SECRET_KEY=cryptographically-secure-random-string
✓ DEBUG=False
✓ ALLOWED_ORIGINS=production-frontend-domain
✓ ALLOWED_HOSTS=production-domain
✓ LOG_LEVEL=INFO
```

### Optional Variables
```
✓ DB_POOL_SIZE=20
✓ DB_MAX_OVERFLOW=10
✓ DB_POOL_TIMEOUT=30
```

**Note:** Each platform (Heroku, Railway, Render, etc.) has its own method for setting environment variables. Refer to platform documentation.

---

## Rollback Plan

If deployment fails:

1. **Identify the issue** from logs
2. **For code issues:**
   - Revert to previous commit: `git revert HEAD`
   - Push to trigger redeployment
   - Platform will automatically redeploy

3. **For database issues:**
   - Restore from backup if critical
   - Contact platform support if data corrupted

4. **For infrastructure issues:**
   - Consult platform status page
   - Contact platform support

---

## Performance Optimization Checklist

- [ ] GZIPMiddleware enabled (reduces response size ~70%)
- [ ] Database connection pooling configured
- [ ] Static files cached properly (Cache-Control headers)
- [ ] API endpoints optimized (no N+1 queries)
- [ ] Response times < 500ms for most endpoints
- [ ] Database indexes optimized
- [ ] No unnecessary database queries in loops

---

## Success Indicators

Once deployed, confirm:
- ✅ Application accessible from production URL
- ✅ User registration working
- ✅ User login working
- ✅ Protected endpoints require authentication
- ✅ JWT tokens expire correctly
- ✅ Passwords hashed securely
- ✅ CORS headers present in responses
- ✅ Static files serving correctly
- ✅ SSL/HTTPS working
- ✅ Health check endpoint returning 200 OK
- ✅ No errors in application logs
- ✅ Response times acceptable
- ✅ Database connected and accessible

---

**Deployment completed successfully when all items checked! 🚀**
