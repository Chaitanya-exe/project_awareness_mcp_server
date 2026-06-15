from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from .config import Base
from datetime import datetime, timezone

class Project(Base):

    __tablename__ = "projects"

    name = Column(String, nullable=False, primary_key=True)
    path = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) )

    def to_dict(self):
        return {
            "name": self.name,
            "path": self.path,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class ActiveProject(Base):

    __tablename__ = "active_project"

    id = Column(Integer, primary_key=True, default=1)

    project_name = Column(String, ForeignKey("projects.name", ondelete="SET NULL"), nullable=True )
    project = relationship("Project", lazy="joined")