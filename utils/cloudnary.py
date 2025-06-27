import cloudinary.uploader
from fastapi import UploadFile

async def upload_to_cloudinary(file: UploadFile, folder: str = "uploads"):
    result = cloudinary.uploader.upload(
        file.file,
        folder=folder,
        resource_type="auto"
    )
    return result
