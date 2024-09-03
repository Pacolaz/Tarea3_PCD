from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    user_email = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=True)
    recommendations = Column(JSON)
    zip = Column(String, nullable=True)
