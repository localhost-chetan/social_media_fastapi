-- Create votes table
-- depends: 20261029_01_pS5Z9-add-user-id-in-posts-table-as-a-foreign-key

CREATE TABLE IF NOT EXISTS public.votes (
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    PRIMARY KEY (post_id, user_id),
    
    CONSTRAINT votes_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts (id) ON DELETE CASCADE,
    CONSTRAINT votes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users (id) ON DELETE CASCADE
);


ALTER TABLE public.votes
ALTER COLUMN created_at TYPE TIMESTAMPTZ;