from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID
from datetime import datetime
from typing import Optional, Literal, Dict, Any

# Metadata model for JSON fields
class UserMetadata(BaseModel):
    """Metadata stored as JSON in the database"""
    designation: Literal["student", "academic_staff", "non_academic_staff"]
    age: int = Field(..., ge=1, le=150)
    gender: Literal["male", "female", "other", "prefer_not_to_say"]
    dtu_id_number: str
    dtu_email: Optional[EmailStr] = None  # Moved to metadata
    course_and_year_of_study: Optional[str] = None  # Moved to metadata

    class Config:
        extra = "allow" 


# Base User model (what gets returned from DB)
class User(BaseModel):
    uuid: UUID
    registered_email: EmailStr
    name: str
    hash: Optional[str] = None  # Password hash (exclude from responses)
    token: Optional[str] = None  # JWT/session token
    pfp: Optional[str] = None  # Profile picture URL
    email_provider: Optional[Literal["google", "microsoft", "custom"]] = "custom"
    access_level: Literal["user", "admin", "moderator"] = "user"
    metadata: Dict[str, Any]  # JSON field containing designation, age, gender, dtu_id, dtu_email, course_and_year_of_study
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # OAuth specific fields
    oauth_provider: Optional[Literal["google", "microsoft", "github"]] = None
    oauth_id: Optional[str] = None  # Unique ID from OAuth provider
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "registered_email": "student@gmail.com",
                "name": "John Doe",
                "pfp": "https://example.com/profile.jpg",
                "email_provider": "google",
                "access_level": "user",
                "metadata": {
                    "designation": "student",
                    "age": 21,
                    "gender": "male",
                    "dtu_id_number": "2K21/CO/123",
                    "dtu_email": "student@dtu.ac.in",
                    "course_and_year_of_study": "B.Tech CSE - 3rd Year"
                },
                "oauth_provider": "google",
                "oauth_id": "google_12345"
            }
        }


# User response (excludes sensitive fields)
class UserResponse(BaseModel):
    uuid: UUID
    registered_email: EmailStr
    name: str
    pfp: Optional[str] = None
    email_provider: Optional[str] = None
    access_level: str
    metadata: Dict[str, Any]
    created_at: Optional[datetime] = None
    oauth_provider: Optional[str] = None
    
    class Config:
        from_attributes = True


# Create user with normal registration (password already hashed from frontend)
class UserCreate(BaseModel):
    registered_email: EmailStr
    name: str
    hashed_password: str  # Already hashed from frontend
    pfp: Optional[str] = None
    email_provider: Literal["google", "microsoft", "custom"] = "custom"
    access_level: Literal["user", "admin", "moderator"] = "user"
    
    # Metadata fields
    designation: Literal["student", "academic_staff", "non_academic_staff"]
    age: int = Field(..., ge=1, le=150)
    gender: Literal["male", "female", "other", "prefer_not_to_say"]
    dtu_id_number: str
    dtu_email: Optional[EmailStr] = None  # Now in metadata
    course_and_year_of_study: Optional[str] = None  # Now in metadata
    
    @validator('course_and_year_of_study')
    def validate_course_for_students(cls, v, values):
        """Ensure students have course and year information"""
        if values.get('designation') == 'student' and not v:
            raise ValueError('Students must provide course and year of study')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "registered_email": "student@gmail.com",
                "name": "John Doe",
                "hashed_password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                "email_provider": "custom",
                "access_level": "user",
                "designation": "student",
                "age": 21,
                "gender": "male",
                "dtu_id_number": "2K21/CO/123",
                "dtu_email": "student@dtu.ac.in",
                "course_and_year_of_study": "B.Tech CSE - 3rd Year"
            }
        }


# OAuth user creation (no password needed)
class UserCreateOAuth(BaseModel):
    registered_email: EmailStr
    name: str
    pfp: Optional[str] = None
    oauth_provider: Literal["google", "microsoft", "github"]
    oauth_id: str  # Unique ID from OAuth provider
    email_provider: Literal["google", "microsoft", "custom"] = "google"
    access_level: Literal["user", "admin", "moderator"] = "user"
    
    # Metadata fields
    designation: Literal["student", "academic_staff", "non_academic_staff"]
    age: int = Field(..., ge=1, le=150)
    gender: Literal["male", "female", "other", "prefer_not_to_say"]
    dtu_id_number: str
    dtu_email: Optional[EmailStr] = None  # Now in metadata
    course_and_year_of_study: Optional[str] = None  # Now in metadata
    
    @validator('course_and_year_of_study')
    def validate_course_for_students(cls, v, values):
        if values.get('designation') == 'student' and not v:
            raise ValueError('Students must provide course and year of study')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "registered_email": "student@gmail.com",
                "name": "John Doe",
                "pfp": "https://lh3.googleusercontent.com/...",
                "oauth_provider": "google",
                "oauth_id": "google_123456789",
                "email_provider": "google",
                "designation": "student",
                "age": 21,
                "gender": "male",
                "dtu_id_number": "2K21/CO/123",
                "dtu_email": "student@dtu.ac.in",
                "course_and_year_of_study": "B.Tech CSE - 3rd Year"
            }
        }


# User update model
class UserUpdate(BaseModel):
    name: Optional[str] = None
    pfp: Optional[str] = None
    access_level: Optional[Literal["user", "admin", "moderator"]] = None
    
    # Metadata fields (optional updates)
    designation: Optional[Literal["student", "academic_staff", "non_academic_staff"]] = None
    age: Optional[int] = Field(None, ge=1, le=150)
    gender: Optional[Literal["male", "female", "other", "prefer_not_to_say"]] = None
    dtu_id_number: Optional[str] = None
    dtu_email: Optional[EmailStr] = None  # Now in metadata
    course_and_year_of_study: Optional[str] = None  # Now in metadata
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Updated",
                "pfp": "https://example.com/new-profile.jpg",
                "age": 22,
                "dtu_email": "newemail@dtu.ac.in"
            }
        }


# Login request models
class UserLoginCredentials(BaseModel):
    """Login with email and hashed password"""
    email: EmailStr
    hashed_password: str  # Already hashed from frontend
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "student@gmail.com",
                "hashed_password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
            }
        }


class UserLoginOAuth(BaseModel):
    """Login with OAuth token"""
    oauth_provider: Literal["google", "microsoft", "github"]
    oauth_token: str  # JWT token from OAuth provider
    oauth_id: str  # Unique ID from OAuth provider
    
    class Config:
        json_schema_extra = {
            "example": {
                "oauth_provider": "google",
                "oauth_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6...",
                "oauth_id": "google_123456789"
            }
        }


# Token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "uuid": "123e4567-e89b-12d3-a456-426614174000",
                    "registered_email": "student@gmail.com",
                    "name": "John Doe"
                }
            }
        }


# Password update (for normal auth users only)
class PasswordUpdate(BaseModel):
    old_hashed_password: str  # Current password (already hashed)
    new_hashed_password: str  # New password (already hashed)
    
    class Config:
        json_schema_extra = {
            "example": {
                "old_hashed_password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                "new_hashed_password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"
            }
        }