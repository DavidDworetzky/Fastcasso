from dataclasses import dataclass
from typing import Optional

@dataclass
class ImageTransformInput:
    """
    Represents an image transform operation
    """
    prompt:str
    name:str
    image_id:int
    height:Optional[int] = None
    width:Optional[int] = None