from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from controllers.file_controller import FileController
from services.vector_service import VectorService
router = APIRouter(prefix="/file", tags=["File"])


@router.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    return FileController.upload(file, background_tasks)


@router.get("/vector-status")
def get_vector_status():
    return FileController.vector_status()

@router.post("/vector-cancel")
def cancel_vector():
    VectorService.cancel()
    return {"message": "Cancellation requested"}
