from fastapi import HTTPException
from sqlalchemy.orm import Session
from services.contact_service import (
    insert_contact,
    get_all_contacts,
    get_contact_count,
)
from schemas.contact_schema import ContactData

def create_contact_controller(db: Session, data: ContactData):
    try:
        return insert_contact(db, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def fetch_contacts_controller(db: Session):
    try:
        return get_all_contacts(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def fetch_count_controller(db: Session):
    try:
        return get_contact_count(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
