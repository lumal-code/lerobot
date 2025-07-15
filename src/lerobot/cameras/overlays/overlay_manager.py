import numpy as np
import cv2

from dataclasses import dataclass
from typing import List, Tuple, Optional

from .configuration_overlay import OverlayConfig

@dataclass
class Box:
    x1: int
    y1: int 
    x2: int
    y2: int
    color: Tuple[int, int, int] = (0, 255, 0)  # Green default
    thickness: int = 2

class OverlayManager:
    """
    Manages the overlay system. Boxes can be modified. TODO: add file parsing from json?
    """
    def __init__(self, config: OverlayConfig):
        self.config = config
        self.boxes: List[Box] = []

    def add_box(self, x1: int, y1: int, x2: int, y2: int, 
            color: Optional[Tuple[int, int, int]] = None, 
            thickness: Optional[int] = None):
        """Add a single box to be drawn"""
        color = color or self.config.box_color
        thickness = thickness or self.config.box_thickness
        self.boxes.append(Box(x1, y1, x2, y2, color, thickness))
    
    def clear_boxes(self):
        """Remove all boxes"""
        self.boxes.clear()
    
    def apply_overlay(self, image: np.ndarray, camera_name: str) -> np.ndarray:
        """ Applies the overlay to the image provided """
        if not self.config.enabled:
            return image

        for box in self.boxes:
            image = cv2.rectangle(
                image, 
                [box.x1, box.y1], 
                [box.x2, box.y2], 
                box.color, 
                box.thickness
                )

        return image