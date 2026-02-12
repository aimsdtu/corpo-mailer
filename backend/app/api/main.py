"""API routes for DTU Mailing Service"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from uuid import UUID
from typing import Any
from app.db.session import get_db_session
from app.db.protocol import Database
from app.api.services.userservice import UserService
from app.api.models.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    PasswordUpdate,
)


router = APIRouter(prefix="/api/v1", tags=["api"])


# ============================================================================
# USER CREATION ENDPOINTS
# ============================================================================

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    db: Database = Depends(get_db_session)
):
    """
    Create a new user with normal authentication (email/password).
    
    - **registered_email**: User's primary email address
    - **name**: Full name of the user
    - **hashed_password**: Pre-hashed password (hash on client side)
    - **designation**: User role (student, faculty, staff, etc.)
    - **age**: User's age
    - **gender**: User's gender
    - **dtu_id_number**: DTU identification number
    """
    service = UserService(db)
    
    # Check if email already exists
    if await service.user_exists(user_create.registered_email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Check if DTU ID already exists
    if await service.check_dtu_id_exists(user_create.dtu_id_number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="DTU ID already registered"
        )
    
    user = await service.create_user(user_create)
    return user

# ============================================================================
# USER RETRIEVAL ENDPOINTS
# ============================================================================

@router.get("/users/{uuid}", response_model=UserResponse)
async def get_user(
    uuid: str,
    db: Database = Depends(get_db_session)
):
    """Get user by UUID"""
    service = UserService(db)
    try:
        user_uuid = UUID(uuid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    user = await service.get_user_by_uuid(user_uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/users", response_model=list[UserResponse])
async def get_all_users(
    db: Database = Depends(get_db_session)
):
    """Get all users (admin only - add auth middleware)"""
    service = UserService(db)
    users = await service.get_all_users()
    return users


# ============================================================================
# USER FILTERING ENDPOINTS
# ============================================================================

@router.get("/users/filter/designation/{designation}", response_model=list[UserResponse])
async def get_users_by_designation(
    designation: str,
    db: Database = Depends(get_db_session)
):
    """
    Get users filtered by designation.
    
    - **designation**: student, faculty, staff, admin, etc.
    """
    service = UserService(db)
    users = await service.get_users_by_designation(designation)
    return users


@router.get("/users/filter/access-level/{access_level}", response_model=list[UserResponse])
async def get_users_by_access_level(
    access_level: str,
    db: Database = Depends(get_db_session)
):
    """
    Get users filtered by access level.
    
    - **access_level**: user, admin, moderator, etc.
    """
    service = UserService(db)
    users = await service.get_users_by_access_level(access_level)
    return users


@router.get("/users/filter/course-year", response_model=list[UserResponse])
async def get_students_by_course_year(
    course: str = Query(..., description="Course name (e.g., CSE, ECE, ME)"),
    year: str = Query(..., description="Year of study (e.g., 1, 2, 3, 4)"),
    db: Database = Depends(get_db_session)
):
    """
    Get students by course and year of study.
    
    - **course**: Course abbreviation (CSE, ECE, ME, etc.)
    - **year**: Year of study (1, 2, 3, 4)
    """
    service = UserService(db)
    users = await service.get_students_by_course_year(course, year)
    return users


# ============================================================================
# USER UPDATE ENDPOINTS
# ============================================================================

@router.patch("/users/{uuid}", response_model=UserResponse)
async def update_user(
    uuid: str,
    user_update: UserUpdate,
    db: Database = Depends(get_db_session)
):
    """
    Update user information (partial update).
    
    All fields are optional - only provided fields will be updated.
    """
    service = UserService(db)
    try:
        user_uuid = UUID(uuid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    user = await service.update_user(user_uuid, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/users/{uuid}/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    uuid: str,
    password_update: PasswordUpdate,
    db: Database = Depends(get_db_session)
):
    """
    Update user password (normal auth users only).
    
    - Requires old password verification
    - Cannot be used for OAuth users
    """
    service = UserService(db)
    try:
        user_uuid = UUID(uuid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    try:
        success = await service.update_password(user_uuid, password_update)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/users/{uuid}/profile-picture", response_model=UserResponse)
async def update_profile_picture(
    uuid: str,
    pfp_url: str = Query(..., description="URL of the new profile picture"),
    db: Database = Depends(get_db_session)
):
    """Update user profile picture"""
    service = UserService(db)
    try:
        user_uuid = UUID(uuid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    user = await service.update_profile_picture(user_uuid, pfp_url)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.patch("/users/{uuid}/metadata", response_model=UserResponse)
async def update_metadata(
    uuid: str,
    metadata_updates: dict[str, Any],
    db: Database = Depends(get_db_session)
):
    """
    Update user metadata fields.
    
    Merges provided fields with existing metadata.
    Accepts any JSON object with metadata fields.
    """
    service = UserService(db)
    try:
        user_uuid = UUID(uuid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    user = await service.update_metadata(user_uuid, metadata_updates)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# ============================================================================
# TOKEN MANAGEMENT ENDPOINTS
# ============================================================================

@router.put("/users/{uuid}/token", response_model=UserResponse)
async def set_user_token(
    uuid: str,
    token: str = Query(..., description="JWT token to set for user"),
    db: Database = Depends(get_db_session)
):
    """Set JWT token for user session"""
    service = UserService(db)
    try:
        user_uuid = UUID(uuid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    user = await service.set_user_token(user_uuid, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/users/{uuid}/regenerate-token", response_model=dict[str, str])
async def regenerate_token(
    uuid: str,
    db: Database = Depends(get_db_session)
):
    """
    Regenerate authentication token for user.
    
    Returns new token string.
    """
    service = UserService(db)
    try:
        user_uuid = UUID(uuid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    new_token = await service.regenerate_token(user_uuid)
    if not new_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"token": new_token}


# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@router.get("/users/stats/count", response_model=dict[str, int])
async def count_users(
    db: Database = Depends(get_db_session)
):
    """Get total count of users"""
    service = UserService(db)
    count = await service.count_users()
    return {"count": count}


@router.get("/users/stats/count/designation/{designation}", response_model=dict[str, int])
async def count_users_by_designation(
    designation: str,
    db: Database = Depends(get_db_session)
):
    """Get count of users by designation"""
    service = UserService(db)
    count = await service.count_users_by_designation(designation)
    return {"count": count, "designation": designation}


# ============================================================================
# USER DELETION ENDPOINTS
# ============================================================================

@router.delete("/users/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    uuid: str,
    db: Database = Depends(get_db_session)
):
    """
    Delete a user (hard delete).
    
    **Warning**: This permanently removes the user from the database.
    """
    service = UserService(db)
    try:
        user_uuid = UUID(uuid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    success = await service.delete_user(user_uuid)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )