# 🔐 FastAPI User Authentication System

A modern, full-stack authentication system with a futuristic glass morphism design. Built with FastAPI backend and responsive HTML5 frontend.

## ✨ Features

- **User Registration & Login** - Secure authentication system
- **JWT Token Authentication** - Session management with bearer tokens
- **Bcrypt Password Hashing** - Industry-standard password security
- **MySQL Database** - SQLAlchemy ORM integration
- **Glass Morphism UI** - Modern, futuristic frontend design
- **Responsive Design** - Mobile, tablet, and desktop compatible
- **Password Strength Indicator** - Real-time password validation
- **Error Handling** - Comprehensive error messages and validation
- **Dashboard** - User profile and token management

## 📋 Project Structure

```
API/
├── main.py                    # FastAPI application entry point
├── auth.py                    # JWT & password authentication utilities
├── database.py                # Database configuration & sessions
├── schemas.py                 # Pydantic validation models
├── requirements.txt           # Python dependencies
├── auth.db                    # SQLite database file
│
├── models/
│   ├── __init__.py
│   └── user.py               # User database model
│
├── services/
│   ├── __init__.py
│   └── auth_service.py       # Business logic layer
│
├── controllers/
│   ├── __init__.py
│   └── auth_controller.py    # API endpoints
│
├── views/
│   ├── __init__.py
│   └── auth_views.py         # Response formatting layer
│
├── static/
│   ├── index.html            # Login/Registration page
│   ├── dashboard.html        # User dashboard
│   ├── css/
│   │   └── style.css         # Futuristic glass morphism styles
│   └── js/
│       ├── auth.js           # Authentication logic
│       └── dashboard.js      # Dashboard functionality
│
├── Dockerfile                # Docker container configuration
├── docker-compose.yml        # Docker Compose setup
├── deploy.sh                 # Deployment script
└── nginx.conf               # Nginx configuration
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- MySQL (or SQLite for testing)

### Installation

1. **Clone/Navigate to project**
```bash
cd API
```

2. **Create virtual environment (Optional but recommended)**
```bash
python -m venv venv
# Activate: venv\Scripts\activate (Windows) or source venv/bin/activate (Linux/Mac)
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run application**
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

5. **Access application**
- Open browser: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`

## 📚 API Endpoints

### Authentication

- `POST /api/v1/register` - Register new user
- `POST /api/v1/login` - Login and get JWT token
- `GET /api/v1/me` - Get current user info (requires auth)

### Pages

- `GET /` - Login/Registration page
- `GET /dashboard` - User dashboard (requires auth)
- `GET /health` - Health check
- `GET /api` - API info

## 🔧 Configuration

Environment variables (.env file):

```env
DATABASE_URL=mysql+pymysql://root:password@localhost/auth_db
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=False
ALLOWED_ORIGINS=*
ALLOWED_HOSTS=*
```

## 🎨 Frontend Features

- **Glass Morphism Design** - Modern semi-transparent cards with blur effects
- **Animated Gradients** - Dynamic text gradients and color transitions
- **Floating Animations** - Background orbs with smooth floating motion
- **Responsive Layout** - Adapts to all screen sizes
- **Dark Theme** - Eye-friendly dark color scheme
- **Icon Integration** - FontAwesome icons for better UX
- **Loading Indicators** - Animated spinners during API calls
- **Alert System** - Toast-like notifications
- **Password Strength** - Real-time validation feedback

## 🔐 Security Features

- **Bcrypt Hashing** - Password securely hashed with bcrypt
- **JWT Authentication** - Stateless token-based auth
- **CORS Protection** - Configurable CORS middleware
- **Trusted Host Middleware** - Host validation in production
- **Password Validation** - Minimum 8 characters required
- **SQL Injection Prevention** - SQLAlchemy parameterized queries
- **Token Expiration** - 30-minute token validity

## 🗄️ Database

Uses SQLAlchemy ORM with support for:
- **MySQL** - Production database
- **SQLite** - Development/testing

User model includes:
- `id` - Unique identifier
- `username` - Unique username
- `email` - Unique email address
- `hashed_password` - Encrypted password
- `is_active` - Account status
- `created_at` - Registration timestamp
- `updated_at` - Last update timestamp

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:8000
```

## 📦 Dependencies

- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy** - ORM
- **PyMySQL** - MySQL connector
- **python-jose** - JWT handling
- **passlib & bcrypt** - Password hashing
- **Pydantic** - Data validation
- **python-multipart** - Form data handling

See `requirements.txt` for full list.

## 🎯 Usage Example

### Register User
```javascript
const response = await fetch('/api/v1/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'john_doe',
    email: 'john@example.com',
    password: 'SecurePass123!'
  })
});
```

### Login
```javascript
const response = await fetch('/api/v1/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'john@example.com',
    password: 'SecurePass123!'
  })
});
const data = await response.json();
localStorage.setItem('authToken', data.access_token);
```

### Protected Request
```javascript
const response = await fetch('/api/v1/me', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
  }
});
```

## 🐛 Troubleshooting

- **Database Connection Error**: Check DATABASE_URL in .env
- **Port Already in Use**: Change port with `--port 8001`
- **Static Files Not Loading**: Verify static/ directory exists
- **401 Unauthorized**: Check token in localStorage

## � Documentation

For detailed information, see:

- **[QUICK_START.md](QUICK_START.md)** - Get running in 5 minutes
- **[GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md)** - Deploy to production (Heroku, Railway, Render, Docker, AWS, etc.)
- **[PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)** - Pre-deployment security and quality checks

## 🌐 Deployment

This application is ready to deploy on:
- ✅ **Heroku** - Easiest option for beginners
- ✅ **Railway** - Modern alternative with GitHub integration
- ✅ **Render** - Free tier with auto-deploy
- ✅ **Docker** - Any platform with Docker support
- ✅ **AWS/DigitalOcean** - Full control and scalability

See [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) for step-by-step instructions for each platform.

## 📝 Production Notes

- ✅ Change `SECRET_KEY` in production (generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- ✅ Set `DEBUG=False` in production
- ✅ Use strong database passwords
- ✅ Configure `ALLOWED_ORIGINS` for your domain
- ✅ Use HTTPS/SSL in production
- ✅ Keep dependencies updated: `pip list --outdated`
- ✅ Store `.env` file securely (never commit to git)
- ✅ Set up database backups
- ✅ Monitor application logs and errors
- ✅ Use `.env.example` template for configuration reference

## 🔑 Key Technologies

| Technology | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.104.1 | Web framework |
| Python | 3.12 | Runtime |
| SQLAlchemy | 2.0.23 | ORM |
| Pydantic | 2.x | Validation |
| python-jose | 3.3.0 | JWT tokens |
| Bcrypt | 5.0.0 | Password hashing |
| Passlib | 1.7.4 | Authentication |
| Uvicorn | 0.24.x | ASGI server |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit pull request

## 📄 License

MIT License - Feel free to use and modify this project for your own purposes.

```

### 4. Environment Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your database credentials:
```env
DATABASE_URL=mysql+pymysql://your_username:your_password@localhost/auth_db
SECRET_KEY=your-super-secret-key-change-this-in-production
```

**Important**: Generate a strong secret key for production:
```bash
openssl rand -hex 32
```

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Register User

**Endpoint**: `POST /api/v1/register`

**Request Body**:
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response** (201 Created):
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2024-01-01T12:00:00"
}
```

**Error Responses**:
- `400 Bad Request`: Email already registered or username taken
- `422 Unprocessable Entity`: Invalid input data

### 2. Login User

**Endpoint**: `POST /api/v1/login`

**Request Body**:
```json
{
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

**Error Responses**:
- `401 Unauthorized`: Incorrect email or password
- `400 Bad Request`: Inactive user account

### 3. Get Current User Info

**Endpoint**: `GET /api/v1/me`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2024-01-01T12:00:00"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or expired token
- `401 Unauthorized`: Token not provided

## Testing with Postman

### 1. Register a New User

1. Create a new request in Postman
2. Set method to `POST`
3. Set URL to `http://localhost:8000/api/v1/register`
4. Go to Body tab, select `raw` and `JSON`
5. Enter the following JSON:
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
}
```
6. Click Send

### 2. Login and Get Token

1. Create a new request in Postman
2. Set method to `POST`
3. Set URL to `http://localhost:8000/api/v1/login`
4. Go to Body tab, select `raw` and `JSON`
5. Enter the following JSON:
```json
{
    "email": "test@example.com",
    "password": "testpass123"
}
```
6. Click Send
7. Copy the `access_token` from the response

### 3. Access Protected Endpoint

1. Create a new request in Postman
2. Set method to `GET`
3. Set URL to `http://localhost:8000/api/v1/me`
4. Go to Headers tab
5. Add a new header:
   - Key: `Authorization`
   - Value: `Bearer <paste_your_token_here>`
6. Click Send

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These provide interactive API documentation where you can test all endpoints directly from your browser.

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Authentication**: Secure token-based authentication
- **Input Validation**: Pydantic models ensure data integrity
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CORS Support**: Configurable Cross-Origin Resource Sharing

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://root:password@localhost/auth_db` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-change-this-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time in minutes | `30` |

## Development Notes

- The API automatically creates database tables on startup
- All passwords are hashed using bcrypt before storage
- JWT tokens expire after 30 minutes by default
- The API includes proper error handling and validation
- CORS is enabled for all origins (configure for production)

## Production Deployment Considerations

1. **Security**:
   - Use a strong, randomly generated `SECRET_KEY`
   - Configure proper CORS origins
   - Use HTTPS in production
   - Set up proper database user permissions

2. **Database**:
   - Use connection pooling
   - Set up database backups
   - Consider using a managed database service

3. **Performance**:
   - Use a production ASGI server like Gunicorn
   - Set up proper logging
   - Consider rate limiting

## License

This project is open source and available under the MIT License.
