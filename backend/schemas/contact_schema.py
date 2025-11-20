from pydantic import BaseModel
from typing import Optional

class ContactData(BaseModel):
    fullname: str
    email: str
    phoneno: Optional[str] = None
    company: Optional[str] = None
    inquirytype: str
    subject: str
    message: str

    class Config:
        from_attributes = True
