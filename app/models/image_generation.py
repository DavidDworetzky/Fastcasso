from dataclasses import dataclass

@dataclass
class ImageGenerationStub:
    prompt:str
    name:str
    id: int

class ImageGeneration:
    prompt:str
    name:str
    id: int
    image:bytes

