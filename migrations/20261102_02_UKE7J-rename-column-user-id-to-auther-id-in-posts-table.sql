-- Rename column user_id to auther_id in posts table
-- depends: 20261102_01_9QOXw-create-votes-table

ALTER TABLE public.posts
RENAME COLUMN user_id TO auther_id;