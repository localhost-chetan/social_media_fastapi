-- Create users table
-- depends: 20261026_01_V0rEP-create-posts-table

CREATE TABLE IF NOT EXISTS public.users(
    id SERIAL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    CONSTRAINT users_email_unique UNIQUE(email)
);