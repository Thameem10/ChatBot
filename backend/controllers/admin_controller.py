from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.admin_schema import AdminCreate, AdminLogin
from services.admin_service import AdminService

class AdminController:

    @staticmethod
    def get_all(db: Session):
        return AdminService.get_all(db)

    @staticmethod
    def get_by_id(db: Session, id: int):
        admin = AdminService.get_by_id(db, id)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return admin

    @staticmethod
    def create(db: Session, data: AdminCreate):
        return AdminService.create(db, data)

    @staticmethod
    def update(db: Session, id: int, data: AdminCreate):
        return AdminService.update(db, id, data)

    @staticmethod
    def delete(db: Session, id: int):
        return AdminService.delete(db, id)

    @staticmethod
    def login(db: Session, data: AdminLogin):
        return AdminService.login(db, data.email, data.password)

    @staticmethod
    def refresh_token(db: Session, refreshToken: str):
        return AdminService.refresh_access_token(db, refreshToken)

    @staticmethod
    def logout(db: Session, adminId: int):
        return AdminService.logout(db, adminId)
