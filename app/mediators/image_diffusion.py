from app.models.image_input import ImageInput
from app.models.image_transform_input import ImageTransformInput
from starlette.responses import StreamingResponse
from typing import Union, List, Optional
from app.pipelines.stable_diffusion import StableDiffusion
from app.pipelines.instruct_pix2pix import InstructPix2Pix
from app.models import settings
from app.models.database.database import Session
from app.models.database.image_input import ImageInput as DBImageInput
from app.models.database.image_output import ImageOutput as DBImageOutput
import io
from app.models.image_generation import ImageGenerationStub
from app.mediators.presets import get_presets
from PIL import Image as PILImage

def generate_image_diffusion(image_input: ImageInput, settings: settings.Settings, preset_id: Optional[int] = None) -> Union[StreamingResponse, str]:
    """
    Outputs an image from a prompt and persists to our database. 
    """
    try:
        available_presets = get_presets(settings)
        keywords = None
        negative_keywords = None
        model_id = settings.simple_diffusion_model_id
        inference_steps = settings.num_inference_steps
        if preset_id is not None:
            preset_id = int(preset_id)
            #get preset from settings
            preset = next((preset for preset in available_presets if preset.preset_id == preset_id), None)
            if preset is not None:
                #set model_id and inference_steps
                model_id = preset.model_id
                inference_steps = preset.inference_steps
                keywords = preset.keywords
                negative_keywords = preset.negative_keywords
                if image_input.height is None:
                    image_input.height = preset.default_height
                if image_input.width is None:
                    image_input.width = preset.default_width
        #modify prompt and negative prompt from preset
        image_input_prompt_text = "" if image_input.prompt is None else image_input.prompt
        image_input_negative_prompt_text = "" if image_input.negative_prompt is None else image_input.negative_prompt
        modified_prompt = f'{keywords} {image_input_prompt_text}' if keywords is not None else image_input.prompt
        modified_negative_prompt = f'{negative_keywords} {image_input_negative_prompt_text}' if negative_keywords is not None else image_input.negative_prompt
        image_input.prompt = modified_prompt
        image_input.negative_prompt = modified_negative_prompt
        #persist image input for job
        db_image_input = DBImageInput(prompt=modified_prompt, name=image_input.name, model_id=model_id, negative_prompt = modified_negative_prompt)
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

def generate_pix2pix_transform(image_transform_input: ImageTransformInput,  settings: settings.Settings) -> Union[StreamingResponse, str]:
    """
    Generates a pix2pix transformation of an image.
    pix2pix is done without presets or prefixes.
    """
    try:
        pix2pix_model = "timbrooks/instruct-pix2pix"
        #persist image input for job
        db_image_input = DBImageInput(prompt=image_transform_input.prompt, name=image_transform_input.name, model_id=pix2pix_model, negative_prompt = "")
        Session.add(db_image_input)
        Session.commit()
        #generate image
        pix2pix = (
        InstructPix2Pix(
            pix2pix_model,
            settings.simple_diffusion_device, 
            settings.safety_check,
            )
        )
        #grab image to do image2image transform on.
        db_image_output = Session.query(DBImageOutput).filter(DBImageOutput.image_output_id == image_transform_input.image_id).first()
        to_transform_image = PILImage.open(io.BytesIO(db_image_output.image_output_blob))
        image = pix2pix.generate(image_transform_input, to_transform_image)
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



def get_image_stubs(page: int, pageSize: int) -> Union[List[ImageInput], str]:
    """
    Returns a list of image stubs from the database.
    """
    try:
        #parse page and pagesize
        page = int(page)
        pageSize = int(pageSize)
        db_image_outputs = Session.query(DBImageOutput).order_by(DBImageOutput.image_input_id.desc()).offset(page*pageSize).limit(pageSize).all()
        image_stubs = []
        for db_image_output in db_image_outputs:
            input = db_image_output.image_input
            image_stubs.append(ImageGenerationStub(prompt=input.prompt, name=input.name, id=db_image_output.image_output_id, model_id=input.model_id, created_at=db_image_output.created_at))
        return image_stubs
    except Exception as e:
        return f"{e}"

def search_image_stubs(term:str, page:int, page_size: int, model_id: Optional[str], negative_prompt: Optional[str]) -> Union[List[ImageInput], str]:
    """
    Returns a list of image stubs from the database.
    """
    try:
        db_image_outputs = Session.query(DBImageOutput).join(DBImageInput)

        if model_id is not None:
            db_image_outputs = db_image_outputs.filter(DBImageInput.model_id == model_id)
        if negative_prompt is not None:
            db_image_outputs = db_image_outputs.filter(DBImageInput.negative_prompt.like(f'%{negative_prompt}%'))
        if term is not None:
            db_image_outputs = db_image_outputs.filter(DBImageInput.prompt.like(f'%{term}%'))
        db_image_outputs = db_image_outputs.offset(page*page_size).limit(page_size).all()
        image_stubs = []
        for db_image_output in db_image_outputs:
            input = db_image_output.image_input
            image_stubs.append(ImageGenerationStub(prompt=input.prompt, name=input.name, id=db_image_output.image_output_id, model_id=input.model_id, created_at= db_image_output.created_at))
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