from app.models.image_input import ImageInput
from starlette.responses import StreamingResponse
from typing import Union
from app.pipelines.stable_diffusion import StableDiffusion
from app.models import settings
import io

def generate_image_diffusion(image_input: ImageInput, settings: settings.Settings) -> Union[StreamingResponse, str]:
    """
    Outputs an image from a prompt and persists to our database. 
    """
    try:
        stable_diffusion = (
        StableDiffusion(
            settings.simple_diffusion_model_id, 
            settings.simple_diffusion_device, 
            settings.safety_check,
            settings.num_inference_steps
            )
        )
        image = stable_diffusion.generate(image_input)
        return StreamingResponse(io.BytesIO(image.tobytes()), media_type="image/png")

    except Exception as e:
        return f"{e}"
