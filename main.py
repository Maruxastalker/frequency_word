from fastapi import FastAPI

from app.api.routes.report import router as public_router

app = FastAPI(title="Frequency Report API")

app.include_router(public_router)


@app.get("/")
async def root():
    return {"message": "Frequency Report API", "status": "running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8060,
    )