from sqlalchemy import Column, Integer, String, DateTime
from app.models.database.database import Base
from app.models.database.job import Job
from datetime import datetime
from uuid import getnode as get_mac
import platform
import socket
from app.models.database.database import Session
from app.models.database.job import JobStatus
import time
from app.mediators.image_diffusion import generate_image_diffusion
from app.models.image_input import ImageInput
from app.models import settings
from multiprocessing import Queue

application_settings = settings.Settings()


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

def register_device_and_start_subprocess(self):
    """
    Entrypoint to register our device and start a subprocess to listen for jobs.
    """
    device = Device.from_device()

    #check if device is already registered
    devices = Device.query.filter_by(device_address=device.device_address).all()
    if len(devices) > 0:
        device = devices[0]
        if device.device_status == DeviceStatus.IDLE:
            #set device to busy and begin subprocess listening for jobs.
            device.device_status = DeviceStatus.BUSY
            Session.commit()
            return


    #check if device is already registered
    #if device.device_address in devices:
def process_jobs(self):
    """
    Process jobs from the queue
    """
    while True:
        #get job from queue
        job = Job.query.filter_by(status=JobStatus.PENDING).first()
        if job is None:
            #if there are no jobs, sleep for 5 seconds
            time.sleep(5)
            continue
        #set job status to running
        job.status = JobStatus.RUNNING
        Session.commit()
        #run job
        try:
            #execute diffusion job for job definition in database
            #create image input
            image_input = ImageInput(job.prompt, job.name)
            response = generate_image_diffusion(image_input, application_settings, job.preset_id)
            queue = Queue()
            queue.put((job.name, response))
            #set job status to completed
            job.status = JobStatus.COMPLETED
            Session.commit()
        except Exception as e:
            job.status = JobStatus.FAILED
            Session.commit()