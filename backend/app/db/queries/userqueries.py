"""User database queries"""
from typing import Any
from functools import lru_cache


class UserQueries:
    """Encapsulates all user-related database queries"""

    # Create queries
    CREATE_USER = """
    INSERT INTO users (
        uuid, registered_email, name, hash, pfp, email_provider,
        access_level, metadata, oauth_provider, oauth_id
    ) VALUES (
        :uuid, :registered_email, :name, :hash, :pfp, :email_provider,
        :access_level, :metadata, :oauth_provider, :oauth_id
    )
    RETURNING *
    """

    CREATE_USER_OAUTH = """
    INSERT INTO users (
        uuid, registered_email, name, pfp, email_provider, access_level,
        metadata, oauth_provider, oauth_id
    ) VALUES (
        :uuid, :registered_email, :name, :pfp, :email_provider, :access_level,
        :metadata, :oauth_provider, :oauth_id
    )
    RETURNING *
    """

    # Read queries - Single user
    GET_USER_BY_UUID = """
    SELECT * FROM users WHERE uuid = :uuid
    """

    GET_USER_BY_EMAIL = """
    SELECT * FROM users WHERE registered_email = :email
    """

    GET_USER_BY_DTU_EMAIL = """
    SELECT * FROM users WHERE metadata->>'dtu_email' = :dtu_email
    """

    GET_USER_BY_DTU_ID = """
    SELECT * FROM users WHERE metadata->>'dtu_id_number' = :dtu_id
    """

    GET_USER_BY_TOKEN = """
    SELECT * FROM users WHERE token = :token
    """

    GET_USER_BY_OAUTH = """
    SELECT * FROM users
    WHERE oauth_provider = :oauth_provider AND oauth_id = :oauth_id
    """

    VERIFY_CREDENTIALS = """
    SELECT * FROM users
    WHERE registered_email = :email AND hash = :hash_value
    """

    # Read queries - Multiple users
    GET_ALL_USERS = """
    SELECT * FROM users ORDER BY created_at DESC
    """

    GET_USERS_BY_DESIGNATION = """
    SELECT * FROM users
    WHERE metadata->>'designation' = :designation
    ORDER BY created_at DESC
    """

    GET_USERS_BY_GENDER = """
    SELECT * FROM users
    WHERE metadata->>'gender' = :gender
    ORDER BY created_at DESC
    """

    GET_USERS_BY_ACCESS_LEVEL = """
    SELECT * FROM users
    WHERE access_level = :access_level
    ORDER BY created_at DESC
    """

    GET_STUDENTS_BY_COURSE_YEAR = """
    SELECT * FROM users
    WHERE metadata->>'designation' = 'student'
    AND metadata->>'course_and_year_of_study' LIKE :course_year_pattern
    ORDER BY created_at DESC
    """

    GET_OAUTH_USERS_BY_PROVIDER = """
    SELECT * FROM users
    WHERE oauth_provider = :oauth_provider
    ORDER BY created_at DESC
    """

    GET_ALL_OAUTH_USERS = """
    SELECT * FROM users
    WHERE oauth_provider IS NOT NULL
    ORDER BY created_at DESC
    """

    GET_NORMAL_AUTH_USERS = """
    SELECT * FROM users
    WHERE oauth_provider IS NULL
    ORDER BY created_at DESC
    """

    # Update queries
    UPDATE_USER = """
    UPDATE users
    SET {fields}, updated_at = :updated_at
    WHERE uuid = :uuid
    RETURNING *
    """

    UPDATE_PASSWORD = """
    UPDATE users
    SET hash = :new_hash, updated_at = :updated_at
    WHERE uuid = :uuid AND hash = :old_hash
    RETURNING *
    """

    UPDATE_TOKEN = """
    UPDATE users
    SET token = :token, updated_at = :updated_at
    WHERE uuid = :uuid
    RETURNING token
    """

    SET_USER_TOKEN = """
    UPDATE users
    SET token = :token, updated_at = :updated_at
    WHERE uuid = :uuid
    RETURNING *
    """

    UPDATE_PROFILE_PICTURE = """
    UPDATE users
    SET pfp = :pfp, updated_at = :updated_at
    WHERE uuid = :uuid
    RETURNING *
    """

    UPDATE_METADATA = """
    UPDATE users
    SET metadata = :metadata, updated_at = :updated_at
    WHERE uuid = :uuid
    RETURNING *
    """

    UPDATE_NAME = """
    UPDATE users
    SET name = :name, updated_at = :updated_at
    WHERE uuid = :uuid
    RETURNING *
    """

    UPDATE_ACCESS_LEVEL = """
    UPDATE users
    SET access_level = :access_level, updated_at = :updated_at
    WHERE uuid = :uuid
    RETURNING *
    """

    # Delete queries
    DELETE_USER = """
    DELETE FROM users WHERE uuid = :uuid
    RETURNING uuid
    """

    # Count queries
    COUNT_ALL_USERS = """
    SELECT COUNT(*) as count FROM users
    """

    COUNT_USERS_BY_DESIGNATION = """
    SELECT COUNT(*) as count FROM users
    WHERE metadata->>'designation' = :designation
    """

    # Existence checks
    USER_EXISTS = """
    SELECT 1 FROM users WHERE registered_email = :email LIMIT 1
    """

    CHECK_EMAIL_EXISTS = """
    SELECT COUNT(*) as count FROM users
    WHERE registered_email = :email
    """

    CHECK_DTU_EMAIL_EXISTS = """
    SELECT COUNT(*) as count FROM users
    WHERE metadata->>'dtu_email' = :dtu_email
    """

    CHECK_DTU_ID_EXISTS = """
    SELECT COUNT(*) as count FROM users
    WHERE metadata->>'dtu_id_number' = :dtu_id
    """

    @staticmethod
    def build_update_query(fields: list[str]) -> str:
        """Build dynamic UPDATE query with provided fields"""
        field_assignments = ", ".join(fields)
        return f"""
        UPDATE users
        SET {field_assignments}, updated_at = :updated_at
        WHERE uuid = :uuid
        RETURNING *
        """


@lru_cache()
def get_user_queries() -> UserQueries:
    """Factory function to get UserQueries instance"""
    return UserQueries()