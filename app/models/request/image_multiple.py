from typing import Union, Optional, List

from fastapi import FastAPI
from pydantic import BaseModel


class image_multiple(BaseModel):
    ids: List[str]