from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from app.models.database.database import Base
#Includes column for image output blob and image output id
class Image_Output(Base):
    __tablename__ = 'image_output'
    image_output_id = Column(Integer, primary_key=True)
    image_output_blob = Column(LargeBinary, nullable=False)
    image_input_id = Column(Integer, ForeignKey('image_input.image_input_id'), nullable=False)

