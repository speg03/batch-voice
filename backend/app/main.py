from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, jobs

app = FastAPI(
    title="Batch Voice API",
    description="音声ファイルの文字起こしをバッチ処理で行うWebアプリケーション",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(jobs.router, prefix="/api", tags=["jobs"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)