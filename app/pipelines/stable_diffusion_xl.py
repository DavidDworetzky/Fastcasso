from diffusers import AutoPipelineForText2Image
import torch
from app.models.image_input import ImageInput
import os
import traceback
import sys
from app.pipelines.stable_diffusion_trivial_safety_checker import StableDiffusionTrivialSafetyChecker
from dotenv import load_dotenv
from typing import Any

load_dotenv()

device = os.getenv("DEVICE_TYPE")

class StableDiffusionXL:
    def __init__(self, model_id:str, device:str, flag_safety:bool, num_inference_steps = 50, guidance_scale:float = 7.5):
        self.model_id = model_id
        self.device = device
        self.guidance_scale = guidance_scale
        self.flag_safety = flag_safety
        self.safety_checker = StableDiffusionTrivialSafetyChecker()
        self.num_inference_steps = num_inference_steps

    def generate(self, image_input:ImageInput) -> Any:
        try:
            pipeline_text2image = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
            ).to("cuda")

            prompt = image_input.prompt
            image = pipeline_text2image(prompt=prompt, width = image_input.width, height = image_input.height, negative_prompt=image_input.negative_prompt, guidance_scale=self.guidance_scale, num_inference_steps = self.num_inference_steps).images[0]
            return image
        except Exception as ex:
            self.log_pipeline_error(ex)
            raise ex

    def log_pipeline_error(self, error):
        print(f"Error in StableDiffusion.generate with model_id: {self.model_id}.")
        print(traceback.format_exc())
        print(sys.exc_info()[2])