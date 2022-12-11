from pydantic import BaseSettings
from typing import List, Optional
from app.models.pipeline_preset import PipelinePreset
from dotenv import load_dotenv
import os

load_dotenv()

device = os.getenv("DEVICE_TYPE")

class Settings(BaseSettings):
    app_name: str = "Fastcasso"
    simple_diffusion_model_id: str = "CompVis/stable-diffusion-v1-4"
    simple_diffusion_device:str = device
    safety_check:bool = False
    num_inference_steps:int = 50
    presets: List[PipelinePreset] = (
    [PipelinePreset(model_id="CompVis/stable-diffusion-v1-4", inference_steps=50, preset_id=1, default_width=512, default_height=512),
    PipelinePreset(model_id="runwayml/stable-diffusion-v1-5", inference_steps=50, preset_id=2, default_width=512, default_height=512),
    #quick preset used for testing
    PipelinePreset(model_id="runwayml/stable-diffusion-v1-5", inference_steps=1, preset_id=3, default_width=512, default_height=512),
    #high quality animation preset
    PipelinePreset(model_id="nitrosocke/mo-di-diffusion", inference_steps=50, preset_id=4, default_width=512, default_height = 512),
    #high quality midjourney style preset
    PipelinePreset(model_id="prompthero/midjourney-v4-diffusion", inference_steps=50, preset_id=5, keywords="mdjrny-v4 style", default_width=512, default_height=512),
    PipelinePreset(model_id="prompthero/midjourney-v4-diffusion", inference_steps=50, preset_id=6, keywords="", default_width=512, default_height=512),
    #stable diffusion 2 presets,
    PipelinePreset(model_id="stabilityai/stable-diffusion-2", inference_steps=50,preset_id=7, default_width = 768, default_height= 768, negative_keywords="ugly, boring, bad anatomy, deformed face, deformed hands, deformed limbs"),
    PipelinePreset(model_id="stabilityai/stable-diffusion-2-1-base", inference_steps=50, preset_id=8, default_width = 768, default_height = 768, negative_keywords="ugly, boring, bad anatomy, deformed face, deformed hands, deformed limbs")]
    )
