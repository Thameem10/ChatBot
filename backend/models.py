from sqlalchemy import Column, Integer, String, DateTime, func , ForeignKey , Text
from database import Base
from sqlalchemy.orm import relationship


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

class Thread(Base):
    __tablename__ = "threads"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    messages = relationship("Message", backref="thread", cascade="all, delete")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)
    thread_id = Column(String, ForeignKey("threads.id", ondelete="CASCADE"))
    sender = Column(String)  
    text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ChatbotFile(Base):
    __tablename__ = "chatbot_file"

    id = Column(String, primary_key=True, index=True)  
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())