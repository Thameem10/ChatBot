from fastapi import HTTPException, UploadFile, BackgroundTasks
from services.file_service import FileService
from services.vector_service import VectorService


class FileController:

    @staticmethod
    def upload(file: UploadFile, background_tasks: BackgroundTasks):
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        try:
            # Save file using FileService
            chatbot_file = FileService.upload_file(file)

            # Trigger vector building in background
            background_tasks.add_task(
                VectorService.build_index,
                chatbot_file.filepath
            )

            return {
                "message": "File uploaded successfully. Vector index building started.",
                "file_id": chatbot_file.id
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def vector_status():
        return {
            "status": VectorService.status,
            "progress": VectorService.progress,
            "time_taken": VectorService.time_taken
        }
