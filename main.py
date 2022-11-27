#framework
from fastapi import FastAPI, HTTPException
from app.models.image_input import ImageInput
from typing import Optional
from app.models import settings
from app.mediators.image_diffusion import get_image_stubs
from app.mediators.image_diffusion import get_image_generation
from app.multiprocessing.multiprocessing import register_and_start_device
from app.mediators.job import queue_generate_image_diffusion_job
import uuid
import time

#constants
api_version = 0.1

settings = settings.Settings()
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    #register device for inference jobs
    register_and_start_device(settings)


@app.get('/')
def version():
    return {"Version" : f"{api_version}"}

#preset_id is optional
@app.get("/image/generate/{prompt}/{name}")
async def generate_image_endpoint(prompt, name, preset_id: Optional[int] = None):
    """
    Outputs an image from a prompt.
    """
    #set correlation_id to uuid4
    correlation_id = uuid.uuid4()
    queue_generate_image_diffusion_job(ImageInput(prompt=prompt,name=name), settings=settings, preset_id=preset_id, correlation_id=correlation_id)
    while True:
        #wait for image output to be persisted
        #if image output isn't persisted, sleep for 250 milliseconds and try again
        image_output = get_image_generation(correlation_id)
        if image_output is None:
            time.sleep(0.25)
        else:
            if isinstance(image_output, str):
                raise HTTPException(status_code=500, detail=image_output)
            return image_output

@app.get("/image/page/{page}/pageSize/{pagesize}")
async def get_image_stubs_endpoint(page, pagesize):
    """
    Returns a list of image stubs from the database.
    """
    image_stubs = get_image_stubs(page, pagesize)
    if isinstance(image_stubs, str):
        raise HTTPException(status_code=500, detail=image_stubs)
    return image_stubs

@app.get("/image/{image_output_id}")
async def get_image_generation_endpoint(image_output_id):
    """
    Returns an image from the database.
    """
    image_output = get_image_generation(image_output_id)
    if isinstance(image_output, str):
        raise HTTPException(status_code=500, detail=image_output)
    return image_output

@app.get("/presets")
async def get_presets():
    """
    Returns a list of presets.
    """
    return settings.presets

