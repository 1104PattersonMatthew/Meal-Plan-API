from fastapi import FastAPI
from routers import router

app = FastAPI(
    title="Meal Planner API",
    description="A simple FastAPI project for planning meals and generating a shopping list.",
    version="1.0.0"
)

app.include_router(router)


@app.get("/", summary="Root endpoint")
def root():
    return {"message": "Meal Planner API is running"}


@app.get("/health", summary="Health check")
def health_check():
    return {"status": "ok"}