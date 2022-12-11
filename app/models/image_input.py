from dataclasses import dataclass
from typing import Optional

@dataclass
class ImageInput:
    prompt:str
    name:str
    height:Optional[int] = None
    width:Optional[int] = None
    negative_prompt:Optional[str] = None