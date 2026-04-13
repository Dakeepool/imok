import logging
from sqlalchemy.orm import Session
from datetime import timedelta
from models.user import User
from schemas import UserCreate, UserResponse, UserLogin, Token
from auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from views.auth_views import AuthViews

logger = logging.getLogger(__name__)

class AuthService:
    """Service layer for authentication business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.views = AuthViews()
    
    def register_user(self, user_data: UserCreate) -> UserResponse:
        """Register a new user"""
        
        # Check if user with email already exists
        existing_user_email = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user_email:
            logger.warning(f"Registration failed: Email already exists - {user_data.email}")
            raise ValueError("Email already registered")
        
        # Check if username already exists
        existing_user_username = self.db.query(User).filter(User.username == user_data.username).first()
        if existing_user_username:
            logger.warning(f"Registration failed: Username already taken - {user_data.username}")
            raise ValueError("Username already taken")
        
        try:
            # Hash the password
            hashed_password = get_password_hash(user_data.password)
            
            # Create new user
            db_user = User(
                username=user_data.username,
                email=user_data.email,
                hashed_password=hashed_password
            )
            
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            
            logger.info(f"✓ User registered successfully: {user_data.email}")
            return self.views.format_user_response(db_user.to_dict())
        except Exception as e:
            self.db.rollback()
            logger.error(f"Registration error: {str(e)}")
            raise ValueError(f"Registration failed: {str(e)}")
    
    def authenticate_user(self, user_credentials: UserLogin) -> Token:
        """Authenticate user and return access token"""
        
        try:
            # Find user by email
            user = self.db.query(User).filter(User.email == user_credentials.email).first()
            
            # Verify user exists and password is correct
            if not user or not verify_password(user_credentials.password, user.hashed_password):
                logger.warning(f"Failed login attempt: {user_credentials.email}")
                raise ValueError("Incorrect email or password")
            
            # Check if user is active
            if not user.is_active:
                logger.warning(f"Login attempt by inactive user: {user_credentials.email}")
                raise ValueError("Inactive user")
            
            # Create access token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.email}, expires_delta=access_token_expires
            )
            
            logger.info(f"✓ User authenticated: {user_credentials.email}")
            return self.views.format_token_response(access_token)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise ValueError(f"Authentication failed: {str(e)}")
    
    def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        try:
            return self.db.query(User).filter(User.email == email).first()
        except Exception as e:
            logger.error(f"Error fetching user by email: {str(e)}")
            return None
    
    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        try:
            return self.db.query(User).filter(User.id == user_id).first()
        except Exception as e:
            logger.error(f"Error fetching user by ID: {str(e)}")
            return None
    
    def update_user(self, user_id: int, update_data: dict) -> UserResponse:
        """Update user information"""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                logger.warning(f"Update failed: User not found - ID {user_id}")
                raise ValueError("User not found")
            
            for field, value in update_data.items():
                if hasattr(user, field) and field != 'id' and field != 'hashed_password':
                    setattr(user, field, value)
            
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"✓ User updated: {user.email}")
            return self.views.format_user_response(user.to_dict())
        except Exception as e:
            self.db.rollback()
            logger.error(f"User update error: {str(e)}")
            raise ValueError(f"Update failed: {str(e)}")
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate user account"""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                logger.warning(f"Deactivation failed: User not found - ID {user_id}")
                raise ValueError("User not found")
            
            user.is_active = False
            self.db.commit()
            
            logger.info(f"✓ User deactivated: {user.email}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Deactivation error: {str(e)}")
            raise ValueError(f"Deactivation failed: {str(e)}")

