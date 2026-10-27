from fastapi import FastAPI
from social_media_fastapi.database import pool
from social_media_fastapi.routers.posts import router as posts_router
from social_media_fastapi.routers.users import router as users_router


app = FastAPI()


@app.on_event("startup")
def open_database_pool():
    pool.open(wait=True)
    print("PostgreSQL connection pool is ready")


@app.on_event("shutdown")
def close_database_pool():
    pool.close()
    print("PostgreSQL connection pool closed")


@app.get('/')
def root():
    return {"message": "Hello World"}


app.include_router(router=posts_router)
app.include_router(router=users_router)
