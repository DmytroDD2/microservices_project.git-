
from datetime import datetime
import httpx
import redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import HTTPException


r = redis.Redis(host='redis', port=6379, db=0)


async def fetch_users():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://user-service:8000/user_service/users/")
        response.raise_for_status()
        return response.json()


async def fetch_posts():
    async with httpx.AsyncClient(trust_env=False, verify=False) as client:
        response = await client.get("http://post-service:8000/post_service/posts/")
        response.raise_for_status()
        return response.json()


add_redis = lambda user, user_posts: r.set(f"user:{user['id']}:post_count", len(user_posts))


async def perform_analysis():
    users = await fetch_users()
    posts = await fetch_posts()

    for user in users:
        user_posts = [post for post in posts if post['user_id'] == user['id']]

        add_redis(user, user_posts)


def start_scheduler():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(perform_analysis, 'interval', minutes=10, next_run_time=datetime.now())
    scheduler.start()
