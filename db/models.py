from .config import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Projects(Base):
    __tablename__ = "projects"
    name = Column(String, primary_key=True)
    path = Column(String, nullable=False)

class ActiveProject(Base):
    __tablename__ = "active_project"
    id = Column(Integer, primary_key=True, default=1)
    project_name = Column(String, ForeignKey("projects.name"), nullable=True)
    project = relationship("Projects")

