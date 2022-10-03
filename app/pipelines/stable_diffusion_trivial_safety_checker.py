
from transformers import CLIPConfig
import torch

class StableDiffusionTrivialSafetyChecker(object):
    config_class = CLIPConfig

    def __init__(self):
        print('Safety Checker Initialized.')

    @torch.no_grad()
    def forward(self, clip_input, images):
        return images, False

    def safety_check(self, clip_input, images):
        return self.forward(clip_input, images)