from sqlalchemy import Column, Integer, String, DateTime
from app.models.database.database import Base
from app.models.database.job import JobStatus, Job
from datetime import datetime
from uuid import getnode as get_mac
import platform
import socket
from app.models.database.database import Session
from app.models import settings
import multiprocessing
import time
from app.mediators.image_diffusion import generate_image_diffusion
from app.models.image_input import ImageInput


class DeviceStatus(object):
  IDLE = 0
  BUSY = 1
  UNKNOWN = 2

class Device(Base):
  __tablename__ = 'Device'
  id = Column(Integer, primary_key=True)
  architecture = Column(String(255))
  device_address = Column(String(255))
  device_name = Column(String(255))
  device_status = Column(Integer)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)
  
  def __init__(self, architecture, device_address, device_name):
        self.architecture = architecture
        self.device_address = device_address
        self.device_name = device_name
        self.device_status = DeviceStatus.IDLE
        self.created_at = datetime.datetime.now()

  def from_device():
    #get mac address from python
    mac = get_mac()
    device_address = str(mac)
    architecture = platform.uname()
    device_name = socket.gethostname()

    return Device(architecture, device_address, device_name)



