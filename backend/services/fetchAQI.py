from fastapi import APIRouter, Query, HTTPException
import requests
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("WAQI_KEY")

router = APIRouter()
WAQI_API_TOKEN = key

@router.get("/aqi")
def get_aqi(lat: float = Query(...), lon: float = Query(...)):
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/"
    params = {"token": WAQI_API_TOKEN}

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")

    if data.get("status") != "ok":
        raise HTTPException(status_code=404, detail="No air quality data found near this location.")

    iaqi = data.get("data", {}).get("iaqi", {})

    def extract(pollutant):
        return iaqi.get(pollutant, {}).get("v", None)

    result = {
        "location": data["data"].get("city", {}).get("name"),
        "pm25_ugm3": extract("pm25"),
        "pm10_ugm3": extract("pm10"),
        "co_ppb": extract("co"),
        "no2_ppb": extract("no2"),
        "o3_ugm3": extract("o3"),
        "aqi": data["data"].get("aqi"),
        "dominant_pollutant": data["data"].get("dominentpol"),
        "last_updated": data["data"].get("time", {}).get("s")
    }

    return result