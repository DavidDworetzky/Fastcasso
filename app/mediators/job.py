from typing import Optional, Any
from app.models.image_input import ImageInput
from app.models import settings
from app.models.database.database import Session
from app.models.database.job import Job
from app.models.database.job import JobStatus
import datetime
from app.models.database.image_input import ImageInput as DBImageInput
from app.models.database.device import Device
from app.mediators.image_diffusion import generate_image_diffusion
import time


def queue_generate_image_diffusion_job(image_input: ImageInput, settings: settings.Settings, preset_id: Optional[int] = None, correlation_id = Optional[Any]) -> None:
    """
    Queues a job for image generation.
    """
    #TODO, refactor common code from this method and generate_image_diffusion into its own mediator method
    model_id = settings.simple_diffusion_model_id
    if preset_id is not None:
        preset_id = int(preset_id)
        #get preset from settings
        preset = next((preset for preset in settings.presets if preset.preset_id == preset_id), None)
        if preset is not None:
            #set model_id and inference_steps
            model_id = preset.model_id

    db_image_input = DBImageInput(prompt=image_input.prompt, name=image_input.name, model_id=model_id, correlation_id=correlation_id)
    Session.add(db_image_input)
    job = Job(prompt=image_input.prompt, 
              name = image_input.name,settings=settings, 
              preset_id=preset_id, status = JobStatus.PENDING, 
              device_id = None, 
              created_at = datetime.datetime.now(), 
              updated_at = datetime.datetime.now()
              )
    Session.add(job)
    Session.commit()
