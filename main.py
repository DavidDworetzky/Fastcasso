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
import cv2


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
    try:
        input = ImageInput(prompt, name)
        stable_diffusion = (
        StableDiffusion(
            settings.simple_diffusion_model_id, 
            settings.simple_diffusion_device, 
            settings.safety_check
            )
        )
        image = stable_diffusion.generate(input)
        return StreamingResponse(io.BytesIO(image.tobytes()), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")

