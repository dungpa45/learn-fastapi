''' SQLAlchemy models for User, Task, and Company '''
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Company(Base):
    ''' Company model representing a company entity, with relationship to users '''
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    mode = Column(String)  # e.g., "public", "private"
    rating = Column(Integer)  # e.g., 1 (low) to 5 (high)
    # relationships to User
    users = relationship("User", back_populates="company")


class User(Base):
    ''' User model representing application users, with relationships to tasks and company '''
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # hashed password
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive
    is_admin = Column(Integer, default=0)  # 1 for admin
    # relationships to Task
    tasks = relationship("Task", back_populates="user")
    # relationships to Company
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)  # foreign key to Company
    company = relationship("Company", back_populates="users")


class Task(Base):
    ''' Task model representing tasks assigned to users, 
    with relationship to users '''
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    summary = Column(String, index=True) # brief summary
    description = Column(String, index=True) # detailed description
    status = Column(String, index=True)  # e.g., "pending", "in-progress", "completed"
    priority = Column(Integer, index=True)  # e.g., 1 (high) to 5 (low)
    # relationships to User
    user_id = Column(Integer, ForeignKey("users.id"))  # foreign key to User
    user = relationship("User", back_populates="tasks")
