import PIL
import requests
import torch
from diffusers import StableDiffusionInstructPix2PixPipeline
from dotenv import load_dotenv
from typing import Any
from app.models.image_transform_input import ImageTransformInput
import os
import traceback
import sys

class InstructPix2Pix:
    def __init__(self, model_id:str, device:str, flag_safety:bool, num_inference_steps = 50, guidance_scale:float = 7.0):
        self.model_id = model_id
        self.device = device
        self.guidance_scale = guidance_scale
        self.flag_safety = flag_safety
        self.num_inference_steps = num_inference_steps

    def generate(self, image_input:ImageTransformInput, image) -> Any:
        try:

            load_dotenv()
            device = os.getenv("DEVICE_TYPE")

            model_id = "timbrooks/instruct-pix2pix"
            pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id).to(device)
            edit = pipe(image_input.prompt, image=image, num_inference_steps=self.num_inference_steps, guidance_scale=1.5, image_guidance_scale=self.guidance_scale).images[0]
            return edit
        except Exception as ex:
            self.log_pipeline_error(ex)
            raise ex



    def log_pipeline_error(self, error):
        print(f"Error in StableDiffusion.generate with model_id: {self.model_id}.")
        print(traceback.format_exc())
        print(sys.exc_info()[2])