from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers or route functions
from backend.ai.aiAPI import router as ai_router
from backend.services.fetchAQI import router as aqi_router

app = FastAPI(title="PollutionViz API")

# CORS setup to allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai_router, prefix="/ai", tags=["AI"])
app.include_router(aqi_router, prefix="/aqi", tags=["AQI"])

@app.get("/")
def root():
    return {"message": "Welcome to PollutionViz backend!"}