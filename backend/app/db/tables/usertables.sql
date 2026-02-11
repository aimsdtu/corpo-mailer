-- Create users table
CREATE TABLE IF NOT EXISTS users (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    registered_email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    hash VARCHAR(255),  -- Password hash (NULL for OAuth users)
    token TEXT,  -- JWT token
    pfp TEXT,  -- Profile picture URL
    email_provider VARCHAR(50) DEFAULT 'custom',
    access_level VARCHAR(50) DEFAULT 'user',
    metadata JSONB NOT NULL DEFAULT '{}',  -- Contains: designation, age, gender, dtu_id_number, dtu_email, course_and_year_of_study
    oauth_provider VARCHAR(50),  -- google, microsoft, github
    oauth_id VARCHAR(255),  -- Unique ID from OAuth provider
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(registered_email);
CREATE INDEX IF NOT EXISTS idx_users_token ON users(token);
CREATE INDEX IF NOT EXISTS idx_users_oauth ON users(oauth_provider, oauth_id);
CREATE INDEX IF NOT EXISTS idx_users_metadata_dtu_email ON users((metadata->>'dtu_email'));
CREATE INDEX IF NOT EXISTS idx_users_metadata_dtu_id ON users((metadata->>'dtu_id_number'));
CREATE INDEX IF NOT EXISTS idx_users_metadata_designation ON users((metadata->>'designation'));

-- Add unique constraint for OAuth users
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_oauth_unique 
ON users(oauth_provider, oauth_id) 
WHERE oauth_provider IS NOT NULL;

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();