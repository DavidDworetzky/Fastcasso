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

#constants
api_version = 0.1

settings = settings.Settings()
app = FastAPI()
	

@app.get('/')
def version():
    return {"Version" : f"{api_version}"}


@app.get("/image/generate/{prompt}/{name}")
async def generate_image(prompt, name):
    """
    Outputs an image from a prompt.
    """
    image_output = generate_image_diffusion(ImageInput(prompt=prompt, name=name), settings)
    if isinstance(image_output, str):
        raise HTTPException(status_code=500, detail=image_output)
    return image_output

