from fastapi import FastAPI
from app.api import router as post_service

app = FastAPI(docs_url="/docs", redoc_url=None)

app.include_router(post_service, prefix="/post_service", tags=["post_service"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)