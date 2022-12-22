from typing import Union, Optional

from fastapi import FastAPI
from pydantic import BaseModel

class create_pipeline_preset(BaseModel):
    name: str
    model_id: str
    inference_steps: int
    default_width: int
    default_height: int
    keywords: Optional[str] = None
    negative_keywords: Optional[str] = None