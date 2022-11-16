from dataclasses import dataclass
from typing import Optional

@dataclass
class PipelinePreset:
    preset_id: int
    model_id: str
    inference_steps: int
    keywords: Optional[str] = None

