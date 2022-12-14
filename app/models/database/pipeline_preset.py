import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, DateTime
from sqlalchemy.orm import relationship
from app.models.database.database import Base

class PipelinePreset(Base):
    """
    Database Class used for storing additional pipeline presets
    """
    __tablename__ = 'pipeline_preset'
    pipeline_preset_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    model_id = Column(String, nullable=False)
    inference_steps = Column(Integer, nullable=False)
    default_width = Column(Integer, nullable=False)
    default_height = Column(Integer, nullable=False)
    keywords = Column(String, nullable=True)
    negative_keywords = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)


