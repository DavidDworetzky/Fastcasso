from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from app.models.database.database import Base
class Image_Input(Base):
    __tablename__ = 'image_input'
    image_input_id = Column(Integer, primary_key=True)
    prompt = Column(String, nullable=False)
    name = Column(String, nullable=False)
    model_id = Column(String, nullable=False)