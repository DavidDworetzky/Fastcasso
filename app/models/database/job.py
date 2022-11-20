from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.models.database.database import Base

#Job Status Enum
class JobStatus(object):
  PENDING = 0
  RUNNING = 1
  COMPLETED = 2
  FAILED = 3
  CANCELLED = 4

  class Job(Base):
    __tablename__ = 'Job'
    id = Column(Integer, primary_key=True)
    prompt = Column(String(255))
    name = Column(String(255))
    preset_id = Column(Integer)
    device_id = Column(Integer, ForeignKey('Device.id'))
    status = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)