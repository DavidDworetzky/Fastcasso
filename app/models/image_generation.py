from dataclasses import dataclass

@dataclass
class ImageGenerationStub:
    prompt:str
    name:str
    id: int
    model_id: str

class ImageGeneration:
    prompt:str
    name:str
    id: int
    image:bytes

