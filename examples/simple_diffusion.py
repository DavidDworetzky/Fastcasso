import torch
from torch import autocast
from diffusers import StableDiffusionPipeline

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
device = "cuda"


pipe = StableDiffusionPipeline.from_pretrained(model_id, use_auth_token=True)
pipe = pipe.to(device)

prompt = "a photo of an astronaut riding a horse on mars"
with autocast("cuda"):
    image = pipe(prompt, guidance_scale=7.5)["sample"][0]  
    
image.save("astronaut_rides_horse.png")