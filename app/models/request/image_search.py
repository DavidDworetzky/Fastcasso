from typing import Union, Optional

from fastapi import FastAPI
from pydantic import BaseModel


class image_search(BaseModel):
    term: str
    model_id: Optional[str] = None
    page: int 
    page_size: int
    negative_prompt: Optional[str] = None