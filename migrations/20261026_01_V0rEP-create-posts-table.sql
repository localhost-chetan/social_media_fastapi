-- Create Posts table
-- depends: 

CREATE TABLE IF NOT EXISTS public.posts(
    id SERIAL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    is_published BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY(id)
);
