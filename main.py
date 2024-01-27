from fastapi import FastAPI
from function import *
from pydantic import BaseModel

app = FastAPI()

class Get_health(BaseModel):
    lat: str
    lon: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/get_aqi_info")
async def get_aqi_infoo(data: Get_health):
    response= await get_aqi_info(data.lat, data.lon)
    return {
        "status": "success",
        "data": response
    }


@app.post("/get_health_recommendations")
async def get_health_recommendationsss(data: Get_health):
    response= await get_health_recommendations(data.lat, data.lon)
    return {
        "status": "success",
        "data": response
    }