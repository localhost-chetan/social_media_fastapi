from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from random import randint
from typing import Optional


app = FastAPI()


posts = [
    {
        "id": 1,
        "title": "A quiet morning",
        "content": "Taking a moment to enjoy the first coffee of the day.",
        "published": True,
        "rating": 5,
    },
    {
        "id": 2,
        "title": "Weekend trail walk",
        "content": "Found a new trail and enjoyed a few hours outside.",
        "published": True,
        "rating": 4,
    },
    {
        "id": 3,
        "title": "Book recommendations",
        "content": "What has everyone been reading lately?",
        "published": False,
        "rating": None,
    },
]


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    rating: int | None = None


@app.get('/')
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post.id = randint(3, 30000)
    posts.append(post.dict())
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int):
    for post in posts:
        if post['id'] == id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")
