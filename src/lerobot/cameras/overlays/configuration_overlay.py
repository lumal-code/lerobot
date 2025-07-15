from dataclasses import dataclass

@dataclass
class OverlayConfig():
    """
    Configuration class for the overlay system. This allows camera input to be fed 
    into an overlay system and generate boxes for improved pick-and-place.
    """
    enabled: bool = False
    box_color: tuple[int, int, int] = (0, 0, 255)  # Red
    box_thickness: int = 2