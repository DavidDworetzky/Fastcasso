from app.models.image_input import ImageInput
from starlette.responses import StreamingResponse
from typing import Union, List, Optional
from app.pipelines.stable_diffusion import StableDiffusion
from app.models import settings
from app.models.database.database import Session
from app.models.database.image_input import ImageInput as DBImageInput
from app.models.database.image_output import ImageOutput as DBImageOutput
import io
from app.models.image_generation import ImageGenerationStub

def generate_image_diffusion(image_input: ImageInput, settings: settings.Settings, preset_id: Optional[int] = None) -> Union[StreamingResponse, str]:
    """
    Outputs an image from a prompt and persists to our database. 
    """
    try:
        keywords = None
        model_id = settings.simple_diffusion_model_id
        inference_steps = settings.num_inference_steps
        if preset_id is not None:
            preset_id = int(preset_id)
            #get preset from settings
            preset = next((preset for preset in settings.presets if preset.preset_id == preset_id), None)
            if preset is not None:
                #set model_id and inference_steps
                model_id = preset.model_id
                inference_steps = preset.inference_steps
                keywords = preset.keywords
        modified_prompt = f'{keywords} {image_input.prompt}' if keywords is not None else image_input.prompt
        #persist image input for job
        db_image_input = DBImageInput(prompt=modified_prompt, name=image_input.name, model_id=model_id)
        Session.add(db_image_input)
        Session.commit()
        #generate image
        stable_diffusion = (
        StableDiffusion(
            model_id, 
            settings.simple_diffusion_device, 
            settings.safety_check,
            inference_steps
            )
        )
        image = stable_diffusion.generate(image_input)
        #persist image output for job
        bytes_io_arr = io.BytesIO()
        image.save(bytes_io_arr, format="PNG")
        output_blob = bytes_io_arr.getvalue()
        #set db image output
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
            image_stubs.append(ImageGenerationStub(prompt=input.prompt, name=input.name, id=db_image_output.image_output_id, model_id=input.model_id))
        return image_stubs
    except Exception as e:
        return f"{e}"

def get_image_generation(image_output_id: int) -> Union[StreamingResponse, str]:
    """
    Returns an image from the database.
    """
    try:
        db_image_output = Session.query(DBImageOutput).filter(DBImageOutput.image_output_id == image_output_id).first()
        print(len(db_image_output.image_output_blob))
        return StreamingResponse(io.BytesIO(db_image_output.image_output_blob), media_type="image/png")
    except Exception as e:
        return f"{e}"