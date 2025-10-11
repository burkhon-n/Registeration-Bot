from database import Base
from sqlalchemy import Column, Integer, String, Enum

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    type = Column(Enum("essay", "poem", "song", "art", "craft", "video", name="project_type"), nullable=True)
    project_url = Column(String, nullable=True)