from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.admin_schema import AdminCreate, AdminLogin , RefreshRequest


from controllers.admin_controller import AdminController

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/getAll")
def get_all(db: Session = Depends(get_db)):
    return AdminController.get_all(db)

@router.get("/getById/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    return AdminController.get_by_id(db, id)

@router.post("/createAdmin")
def create_admin(data: AdminCreate, db: Session = Depends(get_db)):
    return AdminController.create(db, data)

@router.put("/updateAdmin/{id}")
def update_admin(id: int, data: AdminCreate, db: Session = Depends(get_db)):
    return AdminController.update(db, id, data)

@router.delete("/deleteAdmin/{id}")
def delete_admin(id: int, db: Session = Depends(get_db)):
    return AdminController.delete(db, id)

@router.post("/login")
def login(data: AdminLogin, db: Session = Depends(get_db)):
    return AdminController.login(db, data)

@router.post("/refresh")
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    return AdminController.refresh_token(db, data.refreshToken)

@router.post("/logout")
def logout(adminId: int, db: Session = Depends(get_db)):
    return AdminController.logout(db, adminId)
