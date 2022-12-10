from dataclasses import dataclass
from typing import Optional

@dataclass
class PipelinePreset:
    preset_id: int
    model_id: str
    inference_steps: int
    default_width: int
    default_height: int
    keywords: Optional[str] = None
    negative_keywords: Optional[str] = None

