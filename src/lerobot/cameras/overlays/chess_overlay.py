import json
from .overlay_manager import OverlayManager, OverlayConfig

class ChessOverlayManager(OverlayManager):
    def __init__(self, config: OverlayConfig, board_config_path: str):
        super().__init__(config)
        self.board_config_path = board_config_path
        self.board_coordinates = self._load_board_config()
        
        # Chess-specific colors
        self.source_color = (255, 0, 0)  # Red
        self.target_color = (0, 0, 255)  # Blue
    
    def _load_board_config(self) -> dict:
        """Load chess board square coordinates from JSON file"""
        try:
            with open(self.board_config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Chess board config not found at {self.board_config_path}")
            return {}
    
    def create_chess_overlay(self, source_square: str, target_square: str):
        """Set chess move overlay (replaces any existing boxes)"""
        self.clear_boxes()  # Clear existing boxes
        
        # Add source square (red)
        if source_square in self.board_coordinates:
            coords = self.board_coordinates[source_square]
            self.add_box(
                coords["top_left"][0], coords["top_left"][1],
                coords["bottom_right"][0], coords["bottom_right"][1],
                color=self.source_color
            )
        
        # Add target square (blue)
        if target_square in self.board_coordinates:
            coords = self.board_coordinates[target_square]
            self.add_box(
                coords["top_left"][0], coords["top_left"][1], 
                coords["bottom_right"][0], coords["bottom_right"][1],
                color=self.target_color
            )