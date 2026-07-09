from pydantic import BaseModel
from typing import Optional, List

class LogBase(BaseModel):
    platform: str
    pattern: str
    contest_name: Optional[str] = None
    contest_date: Optional[str] = None
    is_virtual: bool = False
    link: str
    concept: str
    mistake: str
    learning: str

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

class TemplateBase(BaseModel):
    title: str
    description: str
    code: str
    language: str

class TemplateCreate(TemplateBase):
    pass

class Template(TemplateBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
