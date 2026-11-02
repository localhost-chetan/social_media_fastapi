from social_media_fastapi.dependencies import (
    DbPool, CurrentUser, get_current_user)
from social_media_fastapi.schemas import (VoteSchema, VoteResponseSchema)
from fastapi import (APIRouter, status, HTTPException, Depends, Response)
from social_media_fastapi.repositories import (
    posts as post_repository, votes as vote_repository)


router = APIRouter(
    prefix="/votes",
    tags=["Votes"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=VoteResponseSchema | None,
             responses={status.HTTP_204_NO_CONTENT: {
                 "description": "Vote removed successfully"
             }})
def toggle_vote(vote: VoteSchema, db_pool: DbPool, current_user: CurrentUser):
    with db_pool.connection() as connection:
        with connection.cursor() as cursor:
            post_id = vote.post_id
            user_id = current_user.id

            # check if the post exists
            post = post_repository.get_post_by_id(
                cursor=cursor, id=post_id)

            if post is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Post with id {post_id} doesn't exists")

            # check if the user has already voted on this post
            existing_vote = vote_repository.get_post_vote(
                cursor=cursor, post_id=post_id, user_id=user_id)

            if existing_vote:
                vote_repository.delete_vote(
                    cursor=cursor, post_id=post_id, user_id=user_id
                )

                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                created_post = vote_repository.create_vote(
                    cursor=cursor, post_id=post_id, user_id=user_id)

                return created_post
