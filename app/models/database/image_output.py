from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from app.models.database.database import Base
from typing import Optional
from app.models.database.image_input import ImageInput
#Includes column for image output blob and image output id
class ImageOutput(Base):
    __tablename__ = 'image_output'
    image_output_id = Column(Integer, primary_key=True)
    image_output_blob = Column(LargeBinary, nullable=False)
    image_input_id = Column(Integer, ForeignKey('image_input.image_input_id'), nullable=False)
    image_input: Optional[ImageInput] = relationship("ImageInput", back_populates="image_input_output")

