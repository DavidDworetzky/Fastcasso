import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, DateTime
from app.models.database.database import Base
class ImageInput(Base):
    __tablename__ = 'image_input'
    image_input_id = Column(Integer, primary_key=True)
    prompt = Column(String, nullable=False)
    negative_prompt = Column(String, nullable=True)
    name = Column(String, nullable=False)
    model_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)