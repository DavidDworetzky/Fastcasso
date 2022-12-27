from dataclasses import dataclass
import datetime

@dataclass
class ImageGenerationStub:
    prompt:str
    name:str
    id: int
    model_id: str
    created_at: datetime.datetime

class ImageGeneration:
    prompt:str
    name:str
    id: int
    image:bytes
    created_at: datetime.datetime

