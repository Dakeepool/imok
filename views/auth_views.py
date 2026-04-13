from typing import Dict, Any
from datetime import datetime
from schemas import UserResponse, Token

class AuthViews:
    """View layer for formatting authentication responses"""
    
    @staticmethod
    def format_user_response(user_data: Dict[str, Any]) -> UserResponse:
        """Format user data for API response"""
        return UserResponse(
            id=user_data.get('id'),
            username=user_data.get('username'),
            email=user_data.get('email'),
            is_active=user_data.get('is_active', True),
            created_at=user_data.get('created_at', datetime.utcnow())
        )
    
    @staticmethod
    def format_token_response(access_token: str, token_type: str = "bearer") -> Token:
        """Format token data for API response"""
        return Token(
            access_token=access_token,
            token_type=token_type
        )
    
    @staticmethod
    def format_success_response(message: str, data: Any = None) -> Dict[str, Any]:
        """Format generic success response"""
        response = {"message": message, "status": "success"}
        if data is not None:
            response["data"] = data
        return response
    
    @staticmethod
    def format_error_response(message: str, status_code: int = 400) -> Dict[str, Any]:
        """Format error response"""
        return {
            "message": message,
            "status": "error",
            "status_code": status_code
        }
