from fastapi import FastAPI, HTTPException
from .services import start_scheduler, r

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    start_scheduler()


@app.get("/analytics/{user_id}")
def read_user_post_count(user_id: int):
    post_count = r.get(f"user:{user_id}:post_count")
    if post_count is not None:
        return {"user_id": user_id, "post_count": int(post_count)}
    else:
        raise HTTPException(status_code=404, detail="User data not found")


@app.get("/analytics/")
def read_all_user_post_counts():
    all_user_post_counts = {}
    for key in r.scan_iter("user:*:post_count"):
        user_id = int(key.decode().split(":")[1])
        post_count = int(r.get(key))
        all_user_post_counts[user_id] = post_count
    return all_user_post_counts


@app.get("/")
async def root():
    return {"message": "Analyst service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
