from dataclasses import dataclass

@dataclass
class PipelinePreset:
    preset_id: int
    model_id: str
    inference_steps: int

