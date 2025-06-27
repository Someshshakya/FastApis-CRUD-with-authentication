from fastapi import APIRouter, UploadFile, File
from config.cloudinary import *
from utils.cloudnary import upload_to_cloudinary

router = APIRouter()

@router.post("/upload/")
async def upload_files(file:UploadFile =File(...)):
    try:
        upload_result = await upload_to_cloudinary(file)
        return {
            "url": upload_result["secure_url"],
            "public_id": upload_result["public_id"],
            "resource_type": upload_result["resource_type"]
        }
    except Exception as e:
        return {"error": str(e)}
