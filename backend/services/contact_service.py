from sqlalchemy.orm import Session
from models import ContactForm
from schemas.contact_schema import ContactData

def insert_contact(db: Session, contact: ContactData):
    new_contact = ContactForm(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

def get_all_contacts(db: Session):
    return db.query(ContactForm).order_by(ContactForm.createdAt.desc()).all()

def get_contact_count(db: Session):
    return db.query(ContactForm).count()
