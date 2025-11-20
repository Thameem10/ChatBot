from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class ContactForm(Base):
    __tablename__ = "contact_form"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phoneno = Column(String, nullable=True)
    company = Column(String, nullable=True)
    inquirytype = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    message = Column(String, nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
 

class Admin(Base):
    __tablename__ = "admin"
    __table_args__ = {"schema": "public"}

    adminId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    refreshToken = Column(String, nullable=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
