from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Fastcasso"
    simple_diffusion_model_id: str = "CompVis/stable-diffusion-v1-4"
    simple_diffusion_device:str = "mps"
    safety_check:bool = False
    num_inference_steps:int = 50