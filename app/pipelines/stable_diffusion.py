import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler, DPMSolverMultistepScheduler
from typing import Any

import numpy as np
import torch.nn as nn

from transformers import CLIPConfig
from app.pipelines.stable_diffusion_trivial_safety_checker import StableDiffusionTrivialSafetyChecker
from app.models.image_input import ImageInput

from diffusers.models.attention import BasicTransformerBlock
from fastcore.basics import patch

from dotenv import load_dotenv
import os
import traceback
import sys

load_dotenv()

device = os.getenv("DEVICE_TYPE")

if device == "mps":
    #Patching for Mac M1 
    @patch
    def forward(self:BasicTransformerBlock, x, context=None):
        x = self.attn1(self.norm1(x.contiguous())) + x # <--- added x.contiguous()
        x = self.attn2(self.norm2(x), context=context) + x
        x = self.ff(self.norm3(x)) + x
        return x

class StableDiffusion:
    def __init__(self, model_id:str, device:str, flag_safety:bool, num_inference_steps = 50, guidance_scale:float = 7.5):
        self.model_id = model_id
        self.device = device
        self.guidance_scale = guidance_scale
        self.flag_safety = flag_safety
        self.safety_checker = StableDiffusionTrivialSafetyChecker()
        self.num_inference_steps = num_inference_steps

    def generate(self, image_input:ImageInput) -> Any:
        try:
            #set custom scheduler info depending on if our pipeline needs it
            scheduler = None

            if self.model_id == "stabilityai/stable-diffusion-2":
                scheduler = EulerDiscreteScheduler.from_pretrained(self.model_id, subfolder="scheduler")

            prompt = image_input.prompt
            #pipeline initialization
            if scheduler is not None:
                pipe = StableDiffusionPipeline.from_pretrained(self.model_id, scheduler=scheduler, use_auth_token=True)
            else: 
                pipe = StableDiffusionPipeline.from_pretrained(self.model_id, use_auth_token=True)
            if not self.flag_safety:
                pipe.safety_checker = None

            pipe = pipe.to(self.device)

            #if we are using the 2-1 model, we need to use the DPMSolverMultiStepScheduler
            if self.model_id == "stabilityai/stable-diffusion-2-1-base":
                scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
            #we enable attention slicing for mps to speed up performance on Mac M1 devices
            if self.device == "mps":
                pipe.enable_attention_slicing()
            try:
                image = pipe(prompt, width = image_input.width, height = image_input.height, negative_prompt=image_input.negative_prompt, guidance_scale=self.guidance_scale, num_inference_steps = self.num_inference_steps).images[0]
                return image
            except Exception as ex:
                print(traceback.format_exc())
                # or
                print(sys.exc_info()[2])
                raise ex
        except Exception as ex:
            print ("Error in StableDiffusion.generate with model_id: " + self.model_id)
            print(traceback.format_exc())
            # or
            print(sys.exc_info()[2])
            raise ex
        