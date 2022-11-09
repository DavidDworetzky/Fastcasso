from app.models.image_input import ImageInput
from starlette.responses import StreamingResponse
from typing import Union, List
from app.pipelines.stable_diffusion import StableDiffusion
from app.models import settings
from app.models.database.database import Session
from app.models.database.image_input import ImageInput as DBImageInput
from app.models.database.image_output import ImageOutput as DBImageOutput
import io
from app.models.image_generation import ImageGenerationStub

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

def get_image_stubs(page: int, pagesize: int) -> Union[List[ImageInput], str]:
    """
    Returns a list of image stubs from the database.
    """
    try:
        #parse page and pagesize
        page = int(page)
        pagesize = int(pagesize)
        db_image_outputs = Session.query(DBImageOutput).order_by(DBImageOutput.image_input_id.desc()).offset(page*pagesize).limit(pagesize).all()
        image_stubs = []
        for db_image_output in db_image_outputs:
            input = db_image_output.image_input
            image_stubs.append(ImageGenerationStub(prompt=input.prompt, name=input.name, id=db_image_output.image_output_id))
        return image_stubs
    except Exception as e:
        return f"{e}"

def get_image_generation(image_output_id: int) -> Union[StreamingResponse, str]:
    """
    Returns an image from the database.
    """
    try:
        db_image_output = Session.query(DBImageOutput).filter(DBImageOutput.image_output_id == image_output_id).first()
        return StreamingResponse(io.BytesIO(db_image_output.image_output_blob), media_type="image/png")
    except Exception as e:
        return f"{e}"