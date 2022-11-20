from typing import Optional
from app.models.image_input import ImageInput
from app.models import settings
from app.models.database.database import Session
from app.models.database.job import Job
from app.models.database.job import JobStatus
import datetime


def queue_generate_image_diffusion_job(image_input: ImageInput, settings: settings.Settings, preset_id: Optional[int] = None) -> None:
    """
    Queues a job for image generation.
    """
    job = Job(prompt=image_input.prompt, 
              name = image_input.name,settings=settings, 
              preset_id=preset_id, status = JobStatus.PENDING, 
              device_id = None, 
              created_at = datetime.datetime.now(), 
              updated_at = datetime.datetime.now()
              )
    Session.add(job)
    Session.commit()
