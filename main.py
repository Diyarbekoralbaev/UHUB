from fastapi import FastAPI, File, UploadFile, HTTPException
from function import *
from pydantic import BaseModel
import json
import uuid
import os
from fastapi.staticfiles import StaticFiles
from database import *



app = FastAPI()
FILES_DIRECTORY = "files"
MAX_FILE_SIZE = 20 * 1024 * 1024  # 10 MB limit
ALLOWED_FILE_TYPES = {"image/jpeg", "image/png", "image/jpg", "image/gif", "image/webp", "video/mp4", "video/mpeg", "video/webm", "application/pdf"}

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


@app.post("/upload_file")
async def upload_filee(file: UploadFile = File(...)):
    
    os.makedirs(FILES_DIRECTORY, exist_ok=True)
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file_path = os.path.join(FILES_DIRECTORY, filename)
    
    with open(file_path, "wb") as buffer:
        while content := await file.read(1024):  # Read 1024 bytes at a time
            buffer.write(content)
            
    file_url = f"http://localhost:8000/files/{filename}"
    return {"file_url": file_url}

app.mount("/files", StaticFiles(directory="files"), name="files")

@app.post("/add_request")
async def add_requestt(title: str, description: str, file_url: str):
    try:
        add_request(title, description, file_url)
        return {
            "status": "success",
            "message": "Request added successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        
@app.post("/verify_request")
async def verify_requestt(id: int):
    try:
        verify_request(id)
        return {
            "status": "success",
            "message": "Request verified successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/get_requests")
async def get_requestss():
    try:
        requests = get_requests()
        return {
            "status": "success",
            "data": requests
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/get_verified_requests")
async def get_verified_requestss():
    try:
        requests = get_verified_requests()
        return {
            "status": "success",
            "data": requests
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        
@app.get("/get_unverified_requests")
async def get_unverified_requestss():
    try:
        requests = get_unverified_requests()
        return {
            "status": "success",
            "data": requests
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }