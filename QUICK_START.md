# Quick Start Guide

Get the FastAPI Authentication API running in under 5 minutes.

## Prerequisites
- Python 3.12 or higher
- Git
- pip (Python package manager)

## Development Setup (Local)

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/fluffy-octo-waffle.git
cd fluffy-octo-waffle/API
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your settings (optional for development)
# Default SQLite database will be created automatically
```

### 5. Run Application
```bash
uvicorn main:app --reload
```

Application runs at: `http://127.0.0.1:8000`

### 6. Access Features
- **Frontend:** http://127.0.0.1:8000
- **API Docs:** http://127.0.0.1:8000/docs
- **Alternative Docs:** http://127.0.0.1:8000/redoc

---

## Docker Setup (Local)

### Prerequisites
- Docker installed
- Docker Compose installed

### 1. Build & Run
```bash
docker-compose up --build
```

Application runs at: `http://localhost`

### 2. Stop Services
```bash
docker-compose down
```

### 3. View Logs
```bash
docker-compose logs -f web
```

---

## API Usage Examples

### Register New User
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePassword123"
  }'
```

### Login
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePassword123"
  }'
```

Response includes JWT token:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

### Access Protected Endpoint
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/me" \
  -H "Authorization: Bearer eyJhbGc..."
```

---

## Project Structure

```
.
├── main.py                      # FastAPI application entry point
├── auth.py                      # JWT and password utilities
├── database.py                  # SQLAlchemy database setup
├── schemas.py                   # Pydantic request/response models
│
├── controllers/                 # Route handlers
│   └── auth_controller.py
│
├── models/                      # SQLAlchemy models
│   └── user.py
│
├── services/                    # Business logic
│   └── auth_service.py
│
├── views/                       # Response formatting
│   └── auth_views.py
│
├── static/                      # Frontend files
│   ├── index.html
│   ├── dashboard.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── auth.js
│       └── dashboard.js
│
├── .env.example                 # Configuration template
├── .gitignore                   # Git ignore patterns
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Docker Compose configuration
├── nginx.conf                   # Nginx reverse proxy config
│
├── README.md                    # Project overview
├── GITHUB_DEPLOYMENT.md         # Deployment guide
├── PRODUCTION_CHECKLIST.md      # Pre-deployment checklist
└── QUICK_START.md              # This file
```

---

## Common Commands

### Development
```bash
# Run with auto-reload
uvicorn main:app --reload

# Run on specific port
uvicorn main:app --host 0.0.0.0 --port 8001

# Run with workers (production-like)
uvicorn main:app --workers 4
```

### Database
```bash
# Reset database (deletes all data - development only)
rm auth.db  # SQLite
python main.py  # Recreates tables
```

### Testing
```bash
# Visit API documentation for interactive testing
# http://127.0.0.1:8000/docs

# Or use curl/Postman for API testing
```

### Cleaning
```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete

# Remove virtual environment (start fresh)
rm -rf venv  # Then recreate with python -m venv venv
```

---

## Environment Variables

### Development Defaults
```env
DATABASE_URL=sqlite:///./auth.db
SECRET_KEY=development-secret-key-change-in-production
DEBUG=True
LOG_LEVEL=DEBUG
```

### Production Recommended
```env
DATABASE_URL=mysql+pymysql://user:pass@host:3306/auth_db
SECRET_KEY=<generated-secure-key>
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
LOG_LEVEL=INFO
```

See `.env.example` for all available options.

---

## Troubleshooting

### Port Already in Use
```bash
# Change port
uvicorn main:app --port 8001

# Or kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Dependencies Installation Error
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with verbose output
pip install -v -r requirements.txt

# Clear pip cache if needed
pip cache purge
```

### Database Lock Error
```bash
# SQLite database locked - delete and recreate
rm auth.db
python main.py
```

### CORS Issues
Verify `ALLOWED_ORIGINS` in `.env` matches your frontend domain.

### Authentication Fails
- Check if SECRET_KEY is consistent
- Verify token hasn't expired (30 minutes)
- Ensure Authorization header format: `Bearer <token>`

---

## Next Steps

1. **Explore API Documentation**
   - Visit `http://127.0.0.1:8000/docs` for interactive API explorer
   - Try out endpoints with SwaggerUI

2. **Review Code**
   - Start with `main.py` to understand application structure
   - Check `controllers/auth_controller.py` for API endpoints
   - Review `services/auth_service.py` for business logic

3. **Customize**
   - Add more API endpoints as needed
   - Extend User model with additional fields
   - Create new authentication methods

4. **Deploy**
   - Follow `GITHUB_DEPLOYMENT.md` for deployment options
   - Use `PRODUCTION_CHECKLIST.md` before going live
   - Choose from: Heroku, Railway, Render, Docker, AWS, etc.

5. **Monitor**
   - Set up error tracking (Sentry)
   - Monitor application logs
   - Track performance metrics

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Make sure virtual environment is activated |
| `port 8000 already in use` | Run on different port: `--port 8001` |
| `Database locked` | Close other connections, delete `.db` file |
| `CORS errors` | Update `ALLOWED_ORIGINS` in `.env` |
| `Invalid token` | Token may have expired (30 min), re-login |
| `Connection refused` | Ensure app is running and accessible |

---

## Getting Help

- **API Documentation:** http://127.0.0.1:8000/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **SQLAlchemy Docs:** https://sqlalchemy.org/
- **Docker Docs:** https://docs.docker.com/

---

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

---

**Ready to go! 🚀 Happy coding!**
