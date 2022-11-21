from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from app.models.database.database import Base
import uuid
class ImageInput(Base):
    __tablename__ = 'image_input'
    image_input_id = Column(Integer, primary_key=True)
    prompt = Column(String, nullable=False)
    name = Column(String, nullable=False)
    model_id = Column(String, nullable=False)
    correlation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)