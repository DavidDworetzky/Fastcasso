#framework
import sys
from fastapi import FastAPI, HTTPException
from app.models.image_input import ImageInput
import uvicorn
from typing import Optional
from app.models import settings
import io
from starlette.responses import StreamingResponse
from app.pipelines.stable_diffusion import StableDiffusion
from app.mediators.image_diffusion import generate_image_diffusion
from app.mediators.image_diffusion import get_image_stubs, search_image_stubs
from app.mediators.image_diffusion import get_image_generation
from app.models.request.image_search import image_search

#constants
api_version = 0.1

settings = settings.Settings()
app = FastAPI()

	

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
async def search_image_stubs_endpoint(term):
    """
    Returns a list of image stubs from the database.
    """
    image_stubs = search_image_stubs(term=term)
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

