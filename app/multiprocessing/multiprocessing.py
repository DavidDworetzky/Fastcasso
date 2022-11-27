from app.models.database.device import Device, DeviceStatus
from app.models.settings import Settings
from app.models.image_input import ImageInput
from app.models.database.job import Job, JobStatus
from app.models.database.database import Session
import multiprocessing
import time
from app.mediators.image_diffusion import generate_image_diffusion

def register_and_start_device(settings: Settings):
    """
    Entrypoint to register our device and start a subprocess to listen for jobs.
    """
    device = Device.from_device()

    #check if device is already registered
    devices = Session.query(Device).filter_by(device_address=device.device_address).all()
    if len(devices) > 0:
        device = devices[0]
        if device.device_status == DeviceStatus.IDLE:
            #set device to busy and begin subprocess listening for jobs.
            device.device_status = DeviceStatus.BUSY
            Session.commit()
            process_jobs(device,settings)

    #if device is not registered, register it and begin subprocess listening for jobs.
    Session.add(device)
    device.device_status = DeviceStatus.BUSY
    Session.commit()
    process_jobs(device, settings)

def process_jobs(device: Device, settings: Settings):
    """
    Spawns watcher to process jobs from the queue
    """
    device.device_status = DeviceStatus.BUSY
    Session.commit()

    #set multiprocessing start method to spawn and start process
    print("Starting Process")
    multiprocessing.set_start_method('spawn')
    p = multiprocessing.Process(target=process_jobs_subprocess, args=(device,settings))
    p.start()
    p.join()

def process_jobs_subprocess(device: Device, settings: Settings):
    """
    Watcher subprocess to process jobs from the queue
    """
    print(device)
    print(settings)
    while True:
        #get job from queue
        job = Session.query(Job).filter_by(status=JobStatus.PENDING).first()
        if job is None:
            #if there are no jobs, sleep for 250 milliseconds
            time.sleep(.25)
            continue
        #set job status to running
        job.status = JobStatus.RUNNING
        job.device_id = device.id
        Session.commit()
        #run job
        try:
            #execute diffusion job for job definition in database
            #create image input
            image_input = ImageInput(job.prompt, job.name)
            generate_image_diffusion(image_input, settings, job.preset_id)
            job.status = JobStatus.COMPLETED
            Session.commit()
        except Exception as e:
            print(e)
            job.status = JobStatus.FAILED
            Session.commit()