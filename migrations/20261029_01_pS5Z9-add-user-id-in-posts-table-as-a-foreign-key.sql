-- Add user_id in posts table as a foreign key
-- depends: 20261027_01_2pXyL-create-users-table

ALTER TABLE
    public.posts
ADD COLUMN 
    user_id INTEGER;


ALTER TABLE
    public.posts
ADD CONSTRAINT
    posts_user_id_fkey
FOREIGN KEY
    (user_id)
REFERENCES
    public.users (id)
ON DELETE
    RESTRICT;


ALTER TABLE
    public.posts
ALTER COLUMN
    user_id
SET
    NOT NULL;


CREATE INDEX
    posts_user_id_idx
ON
    public.posts (user_id);