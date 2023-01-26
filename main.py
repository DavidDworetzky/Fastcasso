#framework
import sys
from fastapi import FastAPI, HTTPException
from app.models.image_input import ImageInput
from app.models.image_transform_input import ImageTransformInput
import uvicorn
from typing import Optional
from app.models import settings
import io
from starlette.responses import StreamingResponse
from app.pipelines.stable_diffusion import StableDiffusion
from app.mediators.image_diffusion import generate_image_diffusion
from app.mediators.image_diffusion import generate_pix2pix_transform
from app.mediators.image_diffusion import get_image_stubs, search_image_stubs
from app.mediators.image_diffusion import get_image_generation
from app.models.request.image_search import image_search
from app.mediators.presets import get_presets as get_all_presets, create_pipeline_preset
from app.models.request.create_pipeline_preset import create_pipeline_preset as create_pipeline_preset_request
import logging

#constants
api_version = 0.12
enhanced_logging = False

if enhanced_logging:
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


#initialization
settings = settings.Settings()
app = FastAPI()

	
#routes
@app.get('/')
def version():
    return {"Version" : f"{api_version}"}

#preset_id is optional
@app.get("/image/generate/{prompt}/{name}")
async def generate_image_endpoint(prompt, name, preset_id: Optional[int] = None, negative_prompt: Optional[str] = None, height: Optional[int] = None, width: Optional[int] = None):
    """
    Outputs an image from a prompt.
    """
    image_output = generate_image_diffusion(ImageInput(prompt=prompt, name=name, negative_prompt=negative_prompt, height=height, width=width), settings, preset_id = preset_id)
    if isinstance(image_output, str):
        raise HTTPException(status_code=500, detail=image_output)
    return image_output

#transforms
@app.get("/image/generate/transform/{prompt}/{name}/{image_id}")
async def transform_image_endpoint(prompt, name, image_id, height: Optional[int] = None, width: Optional[int] = None):
    """
    Transforms an image from a prompt.
    """
    image_output = generate_pix2pix_transform(ImageTransformInput(prompt=prompt, name=name, height=height, width=width, image_id=image_id), settings)
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

#search endpoint with pagination parameters
@app.post("/image/search")
async def search_image_stubs_endpoint(search: image_search):
    """
    Returns a list of image stubs from the database.
    """
    image_stubs = search_image_stubs(term=search.term, model_id=search.model_id, page=search.page, page_size=search.page_size, negative_prompt=search.negative_prompt)
    if isinstance(image_stubs, str):
        raise HTTPException(status_code=500, detail=image_stubs)
    return image_stubs

@app.get("/image/search/{term}")
async def search_image_stubs_endpoint(term:str):
    """
    Returns a list of image stubs from the database.
    """
    default_limit = 1000
    image_stubs = search_image_stubs(term=term,page=0, page_size=default_limit, model_id = None, negative_prompt= None)
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
    return get_all_presets(settings)

@app.post("/preset")
async def create_pipeline_preset_endpoint(preset: create_pipeline_preset_request):
    """
    Creates a new preset.
    """
    return create_pipeline_preset(preset)
