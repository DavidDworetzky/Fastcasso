from app.models.database.database import Session
from app.models.database.device import Device
from app.models.database.device import DeviceStatus
from app.models.settings import Settings

def register_and_start_device(settings: Settings):
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
            device.process_jobs(settings)

    #if device is not registered, register it and begin subprocess listening for jobs.
    Session.add(device)
    device.device_status = DeviceStatus.BUSY
    Session.commit()
    device.process_jobs(settings)
