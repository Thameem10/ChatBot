from sqlalchemy.orm import Session
from models import Admin
from schemas.admin_schema import AdminCreate , AdminDetails
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException
import os
from dotenv import load_dotenv

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load .env variables
load_dotenv()

# Now this will NOT be None
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
REFRESH_SECRET = os.getenv("REFRESH_SECRET")
ACCESS_EXPIRY_MINUTES = int(os.getenv("ACCESS_EXPIRY_MINUTES", 1))    
REFRESH_EXPIRY_DAYS = int(os.getenv("REFRESH_EXPIRY_DAYS", 7))


class AdminService:

    @staticmethod
    def get_all(db: Session):
        return db.query(Admin).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(Admin).filter(Admin.adminId == id).first()

    @staticmethod
    def create(db: Session, data: AdminCreate):
        hashed_password = pwd_context.hash(data.password)
        new_admin = Admin(
            name=data.name,
            email=data.email,
            password=hashed_password,
            role=data.role
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin

    @staticmethod
    def update(db: Session, id: int, data: AdminCreate):
        admin = db.query(Admin).filter(Admin.adminId == id).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        admin.name = data.name
        admin.email = data.email
        admin.role = data.role

        if data.password:
            admin.password = pwd_context.hash(data.password)

        db.commit()
        db.refresh(admin)
        return admin

    @staticmethod
    def delete(db: Session, id: int):
        admin = db.query(Admin).filter(Admin.adminId == id).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        db.delete(admin)
        db.commit()
        return {"message": "Admin deleted successfully"}

    @staticmethod
    def login(db: Session, email: str, password: str):
        admin = db.query(Admin).filter(Admin.email == email).first()

        if not admin or not pwd_context.verify(password, admin.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = jwt.encode(
            {"adminId": admin.adminId, "role": admin.role, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRY_MINUTES)},
            ACCESS_SECRET,
            algorithm="HS256"
        )

        refresh_token = jwt.encode(
            {"adminId": admin.adminId, "exp": datetime.utcnow() + timedelta(days=REFRESH_EXPIRY_DAYS)},
            REFRESH_SECRET,
            algorithm="HS256"
        )

        admin.refreshToken = refresh_token
        db.commit()

        return {
            "admin": AdminDetails.from_orm(admin),
            "accessToken": access_token,
            "refreshToken": refresh_token
        }

    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str):
        try:
            decoded = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=["HS256"])
            admin = db.query(Admin).filter(Admin.adminId == decoded["adminId"]).first()

            if not admin or admin.refreshToken != refresh_token:
                raise HTTPException(status_code=403, detail="Invalid refresh token")

            new_access = jwt.encode(
                {"adminId": admin.adminId, "role": admin.role,
                 "exp": datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRY_MINUTES)},
                ACCESS_SECRET,
                algorithm="HS256"
            )

            return {"accessToken": new_access}
        except:
            raise HTTPException(status_code=403, detail="Token expired or invalid")

    @staticmethod
    def logout(db: Session, adminId: int):
        admin = db.query(Admin).filter(Admin.adminId == adminId).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        admin.refreshToken = None
        db.commit()
        return {"message": "Logged out successfully"}
