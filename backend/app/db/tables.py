"""SQLAlchemy table definitions."""
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Index,
    MetaData,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("uuid", UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()),
    Column("registered_email", String(255), unique=True, nullable=False),
    Column("name", String(255), nullable=False),
    Column("hash", String(255)),
    Column("pfp", Text),
    Column("access_level", String(50), nullable=False, server_default="user"),
    Column("metadata", JSONB, nullable=False, server_default="{}"),
    Column("oauth_provider", String(50)),
    Column("oauth_id", String(255)),
    Column("email_verified", Boolean, nullable=False, server_default="false"),
    Column("is_active", Boolean, nullable=False, server_default="true"),
    Column("last_login_at", DateTime(timezone=True)),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
    CheckConstraint(
        "hash IS NOT NULL OR oauth_provider IS NOT NULL",
        name="auth_method_required",
    ),
)
# ---------------- Groups ----------------

groups = Table(
    "groups",
    metadata,

    Column(
        "uuid",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    ),

    Column("name", String(150), nullable=False),

    Column("bio", Text),

    Column(
        "created_by",
        UUID(as_uuid=True),
        nullable=False,
    ),

    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
    ),
)

Index("idx_groups_created_by", groups.c.created_by)


# ---------------- Group Members ----------------

group_members = Table(
    "group_members",
    metadata,

    Column(
        "group_id",
        UUID(as_uuid=True),
        primary_key=True,
    ),

    Column(
        "user_id",
        UUID(as_uuid=True),
        primary_key=True,
    ),

    Column(
        "role",
        String(30),
        nullable=False,
        server_default="user",
    ),

    Column(
        "joined_at",
        DateTime(timezone=True),
        server_default=func.now(),
    ),
)

Index("idx_group_members_user", group_members.c.user_id)
Index("idx_group_members_group", group_members.c.group_id)

# ---------------- Templates ----------------

templates = Table(
    "templates",
    metadata,
    Column(
        "uuid",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    ),
    Column("name", String(255), nullable=False),
    Column("content", Text, nullable=False),
    Column(
        "created_by",
        UUID(as_uuid=True),
        nullable=False,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    ),
)

Index("idx_templates_created_by", templates.c.created_by)
Index("idx_templates_created_at", templates.c.created_at)

# ---------------- Mails ----------------

mails = Table(
    "mails",
    metadata,
    Column(
        "uuid",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    ),
    Column("subject", String(255), nullable=False),
    Column("body", Text, nullable=False),
    Column(
        "template_id",
        UUID(as_uuid=True),
        nullable=True,
    ),
    Column(
        "group_id",
        UUID(as_uuid=True),
        nullable=False,
    ),
    Column(
        "created_by",
        UUID(as_uuid=True),
        nullable=False,
    ),
    Column(
        "status",
        String(30),
        nullable=False,
        server_default="draft",
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
    ),
    Column(
        "sent_at",
        DateTime(timezone=True),
        nullable=True,
    ),
)

Index("idx_mails_created_by", mails.c.created_by)
Index("idx_mails_group_id", mails.c.group_id)
Index("idx_mails_status", mails.c.status)
Index("idx_mails_created_at", mails.c.created_at)

# Partial unique index — one OAuth identity per provider
Index(
    "idx_users_oauth_unique",
    users.c.oauth_provider,
    users.c.oauth_id,
    unique=True,
    postgresql_where=users.c.oauth_provider.isnot(None),
)

# Performance indexes
Index("idx_users_access_level", users.c.access_level)
Index("idx_users_created_at", users.c.created_at)
