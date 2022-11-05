from app.models.image_input import ImageInput
from starlette.responses import StreamingResponse
from typing import Union
from app.pipelines.stable_diffusion import StableDiffusion
from app.models import settings
from app.models.database.database import Session
from app.models.database.image_input import ImageInput as DBImageInput
from app.models.database.image_output import ImageOutput as DBImageOutput
import io

def generate_image_diffusion(image_input: ImageInput, settings: settings.Settings) -> Union[StreamingResponse, str]:
    """
    Outputs an image from a prompt and persists to our database. 
    """
    try:
        #persist image input for job
        db_image_input = DBImageInput(prompt=image_input.prompt, name=image_input.name, model_id=settings.simple_diffusion_model_id)
        Session.add(db_image_input)
        Session.commit()
        #generate image
        stable_diffusion = (
        StableDiffusion(
            settings.simple_diffusion_model_id, 
            settings.simple_diffusion_device, 
            settings.safety_check,
            settings.num_inference_steps
            )
        )
        image = stable_diffusion.generate(image_input)
        #persist image output for job
        output_blob = image.tobytes()
        db_image_output = DBImageOutput(image_input_id=db_image_input.image_input_id, image_output_blob=output_blob) 
        Session.add(db_image_output)
        Session.commit()
        return StreamingResponse(io.BytesIO(output_blob), media_type="image/png")

    except Exception as e:
        return f"{e}"
