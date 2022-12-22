from app.models.request.create_pipeline_preset import create_pipeline_preset
from app.models.database.pipeline_preset import PipelinePreset
from app.models.database.database import Session
from app.models.pipeline_preset import PipelinePreset as PipelinePresetModel
from typing import List
from app.models.settings import Settings

def create_pipeline_preset(preset: create_pipeline_preset) -> PipelinePresetModel:
    """
    Create a new pipeline preset
    """
    db_preset = PipelinePreset(
        name=preset.name,
        model_id=preset.model_id,
        inference_steps=preset.inference_steps,
        default_width=preset.default_width,
        default_height=preset.default_height,
        keywords=preset.keywords,
        negative_keywords=preset.negative_keywords
    )
    Session.add(db_preset)
    Session.commit()
    Session.refresh(db_preset)
    return PipelinePresetModel(preset_id=db_preset.pipeline_preset_id, model_id=db_preset.model_id, inference_steps=db_preset.inference_steps, default_width=db_preset.default_width, default_height=db_preset.default_height, keywords=db_preset.keywords, negative_keywords=db_preset.negative_keywords)

def get_presets(settings : Settings) -> List[PipelinePresetModel]:
    """
    Get all pipeline presets
    """
    #get settings preset length
    settings_preset_length = len(settings.presets)
    #append preset_length to preset_id for custom presets
    db_presets = Session.query(PipelinePreset).all()
    db_preset_models = [PipelinePresetModel(preset_id=db_preset.pipeline_preset_id + settings_preset_length, model_id=db_preset.model_id, inference_steps=db_preset.inference_steps, default_width=db_preset.default_width, default_height=db_preset.default_height, keywords=db_preset.keywords, negative_keywords=db_preset.negative_keywords) for db_preset in db_presets]
    #merge db_preset_models with presets from settings
    for preset in settings.presets:
        if preset not in db_preset_models:
            db_preset_models.append(preset)
    #return db_preset_models sorted by preset_id
    db_preset_models.sort(key=lambda x: x.preset_id)
    return db_preset_models


