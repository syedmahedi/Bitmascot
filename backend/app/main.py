from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from .services import weather as weather_svc
from .services import news as news_svc
from .services import planner as planner_svc

load_dotenv()

app = FastAPI(title="DayMate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Location(BaseModel):
    city: str | None = None
    lat: float | None = None
    lon: float | None = None


@app.get("/")
def read_root():
    return {"message": "DayMate API - FastAPI with OpenWeatherMap & News integration"}


@app.post("/weather")
async def get_weather(loc: Location):
    try:
        q = {"city": loc.city, "lat": loc.lat, "lon": loc.lon}
        result = await weather_svc.fetch_weather(q)
        return {"weather": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/news")
async def get_news(loc: Location):
    try:
        q = {"city": loc.city}
        items = await news_svc.fetch_news(q)
        return {"news": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/plan")
async def get_plan(loc: Location):
    try:
        q = {"city": loc.city, "lat": loc.lat, "lon": loc.lon}
        weather = await weather_svc.fetch_weather(q)
        news = await news_svc.fetch_news(q)
        plan = await planner_svc.generate_plan(weather, news)
        return {"weather": weather, "news": news, "recommendations": plan.get("recommendations", []), "plan_source": plan.get("source")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
