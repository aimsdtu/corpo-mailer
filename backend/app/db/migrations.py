"""Database migrations and schema initialization"""

# SQL schema for users table
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    uuid UUID PRIMARY KEY,
    registered_email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    hash VARCHAR(255),
    token TEXT,
    pfp TEXT,
    email_provider VARCHAR(50) DEFAULT 'custom',
    access_level VARCHAR(50) DEFAULT 'user',
    metadata JSONB DEFAULT '{}',
    oauth_provider VARCHAR(50),
    oauth_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

CREATE_USERS_INDEX_EMAIL = """
CREATE INDEX IF NOT EXISTS idx_users_email
ON users(registered_email);
"""

CREATE_USERS_INDEX_OAUTH = """
CREATE INDEX IF NOT EXISTS idx_users_oauth
ON users(oauth_provider, oauth_id);
"""

CREATE_USERS_INDEX_METADATA_DESIGNATION = """
CREATE INDEX IF NOT EXISTS idx_users_metadata_designation
ON users((metadata->>'designation'));
"""

CREATE_USERS_INDEX_METADATA_DTU_ID = """
CREATE INDEX IF NOT EXISTS idx_users_metadata_dtu_id
ON users((metadata->>'dtu_id_number'));
"""

CREATE_UPDATED_AT_FUNCTION = """
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';
"""

CREATE_UPDATED_AT_TRIGGER = """
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at 
BEFORE UPDATE ON users
FOR EACH ROW 
EXECUTE FUNCTION update_updated_at_column();
"""

# Add more table schemas here as your app grows
CREATE_TEMPLATES_TABLE = """
CREATE TABLE IF NOT EXISTS templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(500) NOT NULL,
    body TEXT NOT NULL,
    created_by UUID REFERENCES users(uuid) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

CREATE_GROUPS_TABLE = """
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_by UUID REFERENCES users(uuid) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

CREATE_GROUP_MEMBERS_TABLE = """
CREATE TABLE IF NOT EXISTS group_members (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(uuid) ON DELETE CASCADE,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(group_id, user_id)
);
"""

CREATE_EMAILS_TABLE = """
CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    sender_id UUID REFERENCES users(uuid) ON DELETE CASCADE,
    subject VARCHAR(500) NOT NULL,
    body TEXT NOT NULL,
    recipients JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""


async def run_migrations(db):
    """Run all database migrations safely"""

    print("🔄 Running database migrations...")

    async def safe_execute(sql: str, success_msg: str, exists_msg: str):
        try:
            await db.execute(sql)
            print(f"  ✅ {success_msg}")
        except Exception as e:
            msg = str(e).lower()

            # Common "already exists" patterns in Postgres
            if (
                "already exists" in msg
                or "duplicate" in msg
                or "exists" in msg
            ):
                print(f"  ⚠️ {exists_msg}")
            else:
                print(f"  ❌ Failed: {success_msg}")
                print(f"     → {e}")
                raise

    # Users
    await safe_execute(
        CREATE_USERS_TABLE,
        "Users table created",
        "Users table already exists"
    )

    await safe_execute(
    CREATE_USERS_INDEX_EMAIL,
    "Index on registered_email created",
    "Index on registered_email already exists"
    )

    await safe_execute(
        CREATE_USERS_INDEX_OAUTH,
        "Index on oauth created",
        "Index on oauth already exists"
    )

    await safe_execute(
        CREATE_USERS_INDEX_METADATA_DESIGNATION,
        "Index on designation created",
        "Index on designation already exists"
    )

    await safe_execute(
        CREATE_USERS_INDEX_METADATA_DTU_ID,
        "Index on dtu_id created",
        "Index on dtu_id already exists"
    )


    await safe_execute(
        CREATE_UPDATED_AT_FUNCTION,
        "Update timestamp function created",
        "Update timestamp function already exists"
    )

    await safe_execute(
        CREATE_UPDATED_AT_TRIGGER,
        "Update timestamp trigger created",
        "Update timestamp trigger already exists"
    )

    # Templates
    await safe_execute(
        CREATE_TEMPLATES_TABLE,
        "Templates table created",
        "Templates table already exists"
    )

    # Groups
    await safe_execute(
        CREATE_GROUPS_TABLE,
        "Groups table created",
        "Groups table already exists"
    )

    # Group Members
    await safe_execute(
        CREATE_GROUP_MEMBERS_TABLE,
        "Group members table created",
        "Group members table already exists"
    )

    # Emails
    await safe_execute(
        CREATE_EMAILS_TABLE,
        "Emails table created",
        "Emails table already exists"
    )

    print("✅ Database migrations finished.")
