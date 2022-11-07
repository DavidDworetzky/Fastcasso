from dataclasses import dataclass

@dataclass
class ImageGenerationStub:
    prompt:str
    name:str

class ImageGeneration:
    prompt:str
    name:str
    image:bytes

