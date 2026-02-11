import json
from uuid import UUID, uuid4
from typing import Optional, Any
from datetime import datetime

from app.api.models.user import (
    User,
    UserCreate,
    UserCreateOAuth,
    UserUpdate,
    UserResponse,
    PasswordUpdate,
)
from app.db.protocol import Database
from app.db.queries.userqueries import get_user_queries


class UserService:
    """Service for managing user operations"""

    def __init__(self, db: Database):
        self.db = db
        self.queries = get_user_queries()

    def _build_metadata(
        self,
        designation: str,
        age: int,
        gender: str,
        dtu_id_number: str,
        dtu_email: Optional[str] = None,
        course_and_year_of_study: Optional[str] = None,
    ) -> dict[str, Any]:
        """Build metadata JSON object"""
        metadata = {
            "designation": designation,
            "age": age,
            "gender": gender,
            "dtu_id_number": dtu_id_number,
        }
        
        # Add optional fields to metadata
        if dtu_email:
            metadata["dtu_email"] = dtu_email
        if course_and_year_of_study:
            metadata["course_and_year_of_study"] = course_and_year_of_study
            
        return metadata

    def _row_to_user(self, row: dict[str, Any]) -> Optional[User]:
        """Convert database row to User model"""
        if not row:
            return None

        metadata = row.get("metadata")
        if isinstance(metadata, str):
            metadata = json.loads(metadata)
        
        return User(
            uuid=UUID(row["uuid"]) if isinstance(row["uuid"], str) else row["uuid"],
            registered_email=row["registered_email"],
            name=row["name"],
            hash=row.get("hash"),
            token=row.get("token"),
            pfp=row.get("pfp"),
            email_provider=row.get("email_provider", "custom"),
            access_level=row.get("access_level", "user"),
            metadata=metadata or {},
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            oauth_provider=row.get("oauth_provider"),
            oauth_id=row.get("oauth_id"),
        )

    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user with normal authentication"""
        user_uuid = uuid4()

        metadata = self._build_metadata(
            designation=user_create.designation,
            age=user_create.age,
            gender=user_create.gender,
            dtu_id_number=user_create.dtu_id_number,
            dtu_email=user_create.dtu_email,
            course_and_year_of_study=user_create.course_and_year_of_study,
        )

        params = {
            "uuid": str(user_uuid),
            "registered_email": user_create.registered_email,
            "name": user_create.name,
            "hash": user_create.hashed_password,
            "pfp": user_create.pfp,
            "email_provider": user_create.email_provider,
            "access_level": user_create.access_level,
            "metadata": json.dumps(metadata),
            "oauth_provider": None,  # ✅ ADD THIS
            "oauth_id": None,        # ✅ ADD THIS
        }

        row = await self.db.fetch_one(self.queries.CREATE_USER, params)
        return self._row_to_user(row)

    async def create_user_oauth(self, user_create_oauth: UserCreateOAuth) -> User:
        """Create a new user with OAuth authentication"""
        user_uuid = uuid4()

        metadata = self._build_metadata(
            designation=user_create_oauth.designation,
            age=user_create_oauth.age,
            gender=user_create_oauth.gender,
            dtu_id_number=user_create_oauth.dtu_id_number,
            dtu_email=user_create_oauth.dtu_email,
            course_and_year_of_study=user_create_oauth.course_and_year_of_study,
        )

        params = {
            "uuid": str(user_uuid),
            "registered_email": user_create_oauth.registered_email,
            "name": user_create_oauth.name,
            "pfp": user_create_oauth.pfp,
            "email_provider": user_create_oauth.email_provider,
            "access_level": user_create_oauth.access_level,
            "metadata": json.dumps(metadata),
            "oauth_provider": user_create_oauth.oauth_provider,
            "oauth_id": user_create_oauth.oauth_id,
        }

        row = await self.db.fetch_one(self.queries.CREATE_USER_OAUTH, params)
        return self._row_to_user(row)

    async def get_user_by_uuid(self, uuid: UUID) -> Optional[User]:
        """Retrieve a user by UUID"""
        row = await self.db.fetch_one(self.queries.GET_USER_BY_UUID, {"uuid": str(uuid)})
        return self._row_to_user(row)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by registered email"""
        row = await self.db.fetch_one(self.queries.GET_USER_BY_EMAIL, {"email": email})
        return self._row_to_user(row)

    async def get_user_by_dtu_email(self, dtu_email: str) -> Optional[User]:
        """Retrieve a user by DTU email (from metadata)"""
        row = await self.db.fetch_one(self.queries.GET_USER_BY_DTU_EMAIL, {"dtu_email": dtu_email})
        return self._row_to_user(row)

    async def get_user_by_dtu_id(self, dtu_id: str) -> Optional[User]:
        """Retrieve a user by DTU ID number (from metadata)"""
        row = await self.db.fetch_one(self.queries.GET_USER_BY_DTU_ID, {"dtu_id": dtu_id})
        return self._row_to_user(row)

    async def get_user_by_oauth_id(self, oauth_provider: str, oauth_id: str) -> Optional[User]:
        """Retrieve a user by OAuth provider and OAuth ID"""
        params = {
            "oauth_provider": oauth_provider,
            "oauth_id": oauth_id
        }
        row = await self.db.fetch_one(self.queries.GET_USER_BY_OAUTH, params)
        return self._row_to_user(row)

    async def update_user(self, uuid: UUID, user_update: UserUpdate) -> Optional[User]:
        """Update user information"""
        # Get current user to merge metadata
        current_user = await self.get_user_by_uuid(uuid)
        if not current_user:
            return None

        # Build metadata updates
        metadata_updates = {}
        if user_update.designation:
            metadata_updates["designation"] = user_update.designation
        if user_update.age:
            metadata_updates["age"] = user_update.age
        if user_update.gender:
            metadata_updates["gender"] = user_update.gender
        if user_update.dtu_id_number:
            metadata_updates["dtu_id_number"] = user_update.dtu_id_number
        if user_update.dtu_email:
            metadata_updates["dtu_email"] = user_update.dtu_email
        if user_update.course_and_year_of_study:
            metadata_updates["course_and_year_of_study"] = user_update.course_and_year_of_study

        merged_metadata = {**current_user.metadata, **metadata_updates}

        # Build dynamic update query
        updates = []
        params = {"uuid": str(uuid)}

        if user_update.name:
            updates.append("name = :name")
            params["name"] = user_update.name
        if user_update.pfp:
            updates.append("pfp = :pfp")
            params["pfp"] = user_update.pfp
        if user_update.access_level:
            updates.append("access_level = :access_level")
            params["access_level"] = user_update.access_level

        if metadata_updates:
            updates.append("metadata = :metadata")
            params["metadata"] = json.dumps(merged_metadata)

        if not updates:
            return current_user

        params["updated_at"] = datetime.utcnow()
        query = self.queries.build_update_query(updates)
        row = await self.db.fetch_one(query, params)
        return self._row_to_user(row)

    async def update_password(self, uuid: UUID, password_update: PasswordUpdate) -> bool:
        """Update user password (only for non-OAuth users)"""
        # First verify the user exists and is not OAuth user
        current_user = await self.get_user_by_uuid(uuid)
        if not current_user:
            return False
        
        if current_user.oauth_provider:
            raise ValueError("Cannot update password for OAuth users")
        
        # Verify old password matches
        if current_user.hash != password_update.old_hashed_password:
            raise ValueError("Incorrect current password")

        params = {
            "uuid": str(uuid),
            "new_hash": password_update.new_hashed_password,
            "old_hash": password_update.old_hashed_password,
            "updated_at": datetime.utcnow(),
        }

        result = await self.db.fetch_one(self.queries.UPDATE_PASSWORD, params)
        return result is not None

    async def set_user_token(self, uuid: UUID, token: str) -> Optional[User]:
        """Set JWT token for user"""
        params = {
            "uuid": str(uuid),
            "token": token,
            "updated_at": datetime.utcnow(),
        }

        row = await self.db.fetch_one(self.queries.SET_USER_TOKEN, params)
        return self._row_to_user(row)

    async def regenerate_token(self, uuid: UUID) -> Optional[str]:
        """Regenerate authentication token for user"""
        import secrets
        new_token = secrets.token_urlsafe(32)
        
        params = {
            "uuid": str(uuid),
            "token": new_token,
            "updated_at": datetime.utcnow(),
        }

        row = await self.db.fetch_one(self.queries.SET_USER_TOKEN, params)
        return row.get("token") if row else None

    async def get_all_users(self) -> list[User]:
        """Get all users"""
        rows = await self.db.fetch_all(self.queries.GET_ALL_USERS)
        return [self._row_to_user(row) for row in rows]

    async def get_users_by_designation(self, designation: str) -> list[User]:
        """Get users filtered by designation (from metadata)"""
        rows = await self.db.fetch_all(
            self.queries.GET_USERS_BY_DESIGNATION, 
            {"designation": designation}
        )
        return [self._row_to_user(row) for row in rows]

    async def get_users_by_access_level(self, access_level: str) -> list[User]:
        """Get users filtered by access level"""
        rows = await self.db.fetch_all(
            self.queries.GET_USERS_BY_ACCESS_LEVEL, 
            {"access_level": access_level}
        )
        return [self._row_to_user(row) for row in rows]

    async def get_users_by_gender(self, gender: str) -> list[User]:
        """Get users filtered by gender (from metadata)"""
        rows = await self.db.fetch_all(
            self.queries.GET_USERS_BY_GENDER, 
            {"gender": gender}
        )
        return [self._row_to_user(row) for row in rows]

    async def get_students_by_course_year(self, course: str, year: str) -> list[User]:
        """Get students by course and year (from metadata)"""
        pattern = f"%{course}%{year}%"
        rows = await self.db.fetch_all(
            self.queries.GET_STUDENTS_BY_COURSE_YEAR,
            {"course_year_pattern": pattern}
        )
        return [self._row_to_user(row) for row in rows]

    async def get_oauth_users(self, oauth_provider: Optional[str] = None) -> list[User]:
        """Get all OAuth users, optionally filtered by provider"""
        if oauth_provider:
            rows = await self.db.fetch_all(
                self.queries.GET_OAUTH_USERS_BY_PROVIDER,
                {"oauth_provider": oauth_provider}
            )
        else:
            rows = await self.db.fetch_all(self.queries.GET_ALL_OAUTH_USERS)
        
        return [self._row_to_user(row) for row in rows]

    async def get_normal_auth_users(self) -> list[User]:
        """Get all users registered with normal authentication (non-OAuth)"""
        rows = await self.db.fetch_all(self.queries.GET_NORMAL_AUTH_USERS)
        return [self._row_to_user(row) for row in rows]

    async def user_exists(self, email: str) -> bool:
        """Check if user exists by email"""
        result = await self.db.fetch_one(self.queries.USER_EXISTS, {"email": email})
        return result is not None

    async def check_email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        result = await self.db.fetch_one(self.queries.CHECK_EMAIL_EXISTS, {"email": email})
        return result.get("count", 0) > 0 if result else False

    async def check_dtu_email_exists(self, dtu_email: str) -> bool:
        """Check if DTU email already exists (from metadata)"""
        result = await self.db.fetch_one(
            self.queries.CHECK_DTU_EMAIL_EXISTS, 
            {"dtu_email": dtu_email}
        )
        return result.get("count", 0) > 0 if result else False

    async def check_dtu_id_exists(self, dtu_id: str) -> bool:
        """Check if DTU ID already exists (from metadata)"""
        result = await self.db.fetch_one(
            self.queries.CHECK_DTU_ID_EXISTS, 
            {"dtu_id": dtu_id}
        )
        return result.get("count", 0) > 0 if result else False

    async def update_profile_picture(self, uuid: UUID, pfp_url: str) -> Optional[User]:
        """Update user profile picture"""
        params = {
            "uuid": str(uuid),
            "pfp": pfp_url,
            "updated_at": datetime.utcnow(),
        }

        row = await self.db.fetch_one(self.queries.UPDATE_PROFILE_PICTURE, params)
        return self._row_to_user(row)

    async def update_metadata(self, uuid: UUID, metadata_updates: dict[str, Any]) -> Optional[User]:
        """Update specific metadata fields"""
        current_user = await self.get_user_by_uuid(uuid)
        if not current_user:
            return None
        
        merged_metadata = {**current_user.metadata, **metadata_updates}
        
        params = {
            "uuid": str(uuid),
            "metadata": json.dumps(merged_metadata),
            "updated_at": datetime.utcnow(),
        }

        row = await self.db.fetch_one(self.queries.UPDATE_METADATA, params)
        return self._row_to_user(row)

    async def count_users(self) -> int:
        """Get total count of users"""
        result = await self.db.fetch_one(self.queries.COUNT_ALL_USERS)
        return result.get("count", 0) if result else 0

    async def count_users_by_designation(self, designation: str) -> int:
        """Get count of users by designation"""
        result = await self.db.fetch_one(
            self.queries.COUNT_USERS_BY_DESIGNATION,
            {"designation": designation}
        )
        return result.get("count", 0) if result else 0

    async def delete_user(self, uuid: UUID) -> bool:
        """Hard delete a user"""
        result = await self.db.fetch_one(self.queries.DELETE_USER, {"uuid": str(uuid)})
        return result is not None