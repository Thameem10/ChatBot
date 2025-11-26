from fastapi import HTTPException, UploadFile
from services.file_service import FileService

class FileController:
    @staticmethod
    def upload(file: UploadFile):
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")
        try:
            return FileService.upload_file(file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
