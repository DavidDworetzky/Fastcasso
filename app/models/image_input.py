from dataclasses import dataclass

@dataclass
class ImageInput:
    prompt:str
    name:str
    negative_prompt:str = None