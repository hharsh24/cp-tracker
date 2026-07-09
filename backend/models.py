from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    logs = relationship("Log", back_populates="owner")
    templates = relationship("Template", back_populates="owner")

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)
    pattern = Column(String, index=True)
    contest_name = Column(String, nullable=True)
    contest_date = Column(String, nullable=True)
    is_virtual = Column(Boolean, default=False)
    link = Column(String)
    concept = Column(Text)
    mistake = Column(Text)
    learning = Column(Text)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="logs")

class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    code = Column(Text)
    language = Column(String, default="cpp")
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="templates")
