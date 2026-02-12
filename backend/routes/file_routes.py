from fastapi import APIRouter, UploadFile, File
from controllers.file_controller import FileController

router = APIRouter(prefix="/file", tags=["File"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return FileController.upload(file)
