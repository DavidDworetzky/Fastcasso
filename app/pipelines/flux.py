import torch
from diffusers import FluxPipeline
from typing import Any

from app.models.image_input import ImageInput

from dotenv import load_dotenv
import os
import traceback
import sys

load_dotenv()

device = os.getenv("DEVICE_TYPE")

class Flux:
    def __init__(self, model_id:str, device:str, flag_safety:bool, num_inference_steps = 50, guidance_scale:float = 7.5):
        self.model_id = model_id
        self.device = device
        self.guidance_scale = guidance_scale
        self.flag_safety = flag_safety
        self.num_inference_steps = num_inference_steps

    def generate(self, image_input:ImageInput) -> Any:
        try:

            pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)
            pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power

            prompt = image_input.prompt

            image = pipe(prompt,
                  height=image_input.height,
                  width=image_input.width,
                  guidance_scale=self.guidance_scale,
                  num_inference_steps=50,
                  max_sequence_length=512,
                  generator=torch.Generator("cpu").manual_seed(0)
                ).images[0]
            return image
        except Exception as ex:
            self.log_pipeline_error(ex)
            raise ex

    def log_pipeline_error(self, error):
        print(f"Error in StableDiffusion.generate with model_id: {self.model_id}.")
        print(traceback.format_exc())
        print(sys.exc_info()[2])