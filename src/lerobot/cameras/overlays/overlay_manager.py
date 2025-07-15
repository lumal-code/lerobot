import numpy as np

from .configuration_overlay import OverlayConfig

class OverlayManager:
    """
    Manages the overlay system. Boxes can be modified. TODO: add file parsing from json?
    """
    def __init__(self, config: OverlayConfig):
        self.config = config
        self.boxes = []
    
    def apply_overlay(self, image: np.ndarray, camera_name: str) -> np.ndarray:
        """ Applies the overlay to the image provided """
        if not self.config.enabled:
            return image

        return image