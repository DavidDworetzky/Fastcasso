import torch
from torch import autocast
from diffusers import StableDiffusionPipeline

import numpy as np
import torch
import torch.nn as nn

from transformers import CLIPConfig
import image_input

inputs = [image_input.image_input(prompt='Waitress at oktoberfest, spring colors, photograph, Munich Germany, 8k, realistic', name = 'interesting1.png'),
image_input.image_input(prompt='New York City in Fall, rainy, times square, realistic', name = 'interesting2.png'),
image_input.image_input(prompt='Angel wreathed in flame with golden armor, unreal engine, high octane render, trending, 8k', name = 'interesting3.png')]


flag_safety = False
class StableDiffusionTrivialSafetyChecker(object):
    config_class = CLIPConfig

    def __init__(self):
        print('Safety Checker Initialized.')

    @torch.no_grad()
    def forward(self, clip_input, images):
        return images, False

    def safety_check(self, clip_input, images):
        return self.forward(clip_input, images)

safety_checker = StableDiffusionTrivialSafetyChecker()

from diffusers.models.attention import BasicTransformerBlock
from fastcore.basics import patch

#Patching for Mac M1 
@patch
def forward(self:BasicTransformerBlock, x, context=None):
    x = self.attn1(self.norm1(x.contiguous())) + x # <--- added x.contiguous()
    x = self.attn2(self.norm2(x), context=context) + x
    x = self.ff(self.norm3(x)) + x
    return x


model_id = "CompVis/stable-diffusion-v1-4"
device = "mps"


pipe = StableDiffusionPipeline.from_pretrained(model_id, use_auth_token=True)
if not flag_safety:
    pipe.safety_checker = safety_checker.safety_check
pipe = pipe.to(device)

for input in inputs:

    prompt = input.prompt
    with autocast("cpu"):
        image = pipe(prompt, guidance_scale=7.5, num_inference_steps = 1).images[0]  
    
        image.save(input.name)