from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.contact_schema import ContactData

from controllers.contact_controller import (
    create_contact_controller,
    fetch_contacts_controller,
    fetch_count_controller,
)
from middlewares.auth_middleware import auth_middleware

router = APIRouter(prefix="/contact", tags=["Contact Form"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create-contact")
def create_contact(data: ContactData, db: Session = Depends(get_db) , user=Depends(auth_middleware)):
    return create_contact_controller(db, data)

@router.get("/")
def get_contacts(db: Session = Depends(get_db) , user=Depends(auth_middleware)):
    return fetch_contacts_controller(db)

@router.get("/count")
def get_count(db: Session = Depends(get_db) , user=Depends(auth_middleware)):
    return fetch_count_controller(db)
