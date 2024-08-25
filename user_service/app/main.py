from fastapi import FastAPI
from app.api import router as user_service
from .services.rabbitmq_service import start_worker

app = FastAPI(docs_url="/docs", redoc_url=None)

app.include_router(user_service, prefix="/user_service", tags=["user_service"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
