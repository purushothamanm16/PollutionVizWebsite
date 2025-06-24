from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import webbrowser
import threading
import time
import os

# Import routers
from backend.ai.aiAPI import router as ai_router
from backend.services.fetchAQI import router as aqi_router

app = FastAPI(title="PollutionViz API")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai_router, prefix="/ai", tags=["AI"])
app.include_router(aqi_router, prefix="/aqi", tags=["AQI"])

# Keep / route as backend root
@app.get("/")
def root():
    return {"message": "Welcome to PollutionViz backend!"}

# Serve frontend at /app
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")

# Auto-open browser to /app
def open_browser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:8000/app")

threading.Thread(target=open_browser).start()
