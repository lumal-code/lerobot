import json
from .overlay_manager import OverlayManager, OverlayConfig

class ChessOverlayManager(OverlayManager):
    def __init__(self, config: OverlayConfig, board_config_path: str):
        super().__init__(config)
        self.board_config_path = board_config_path
        self.board_coordinates = self._load_board_config()
        
        # Chess-specific colors
        self.source_color = (255, 0, 0)  # Red
        self.target_color = (0, 255, 0)  # Green
    
    def _load_board_config(self) -> dict:
        """Load chess board square coordinates from JSON file"""
        try:
            with open(self.board_config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Chess board config not found at {self.board_config_path}")
            return {}
        
    def set_chess_overlay(self) -> bool:
        """
        Interactively set chess overlay.
            
        Returns:
            bool: True if overlay was set, False if skipped
        """
        while True:
            try:
                move_input = input(f"Enter chess move (e.g. 'e2 e4'): ").strip()

                if move_input == "skip":
                    self.clear_boxes()
                    return False
                
                parts = move_input.split()
                if len(parts) != 2:
                    print("Invalid format. Use 'source target' (e.g. 'e2 e4')")
                    continue
                    
                source, target = parts
                
                # Validate squares exist in our config
                if source not in self.board_coordinates:
                    print(f"Unknown square: {source}")
                    continue
                if target not in self.board_coordinates:
                    print(f"Unknown square: {target}")
                    continue
                
                # Apply the overlay
                self.create_chess_overlay(source, target)
                print(f"Chess overlay set: {source} → {target}")
                return True
                
            except KeyboardInterrupt:
                print(f"\nSkipping chess overlay for episode")
                self.clear_boxes()
                return False
            except Exception as e:
                print(f"Error: {e}. Try again.")
    
    def create_chess_overlay(self, source_square: str, target_square: str):
        """Set chess move overlay (replaces any existing boxes)"""
        self.clear_boxes()  # Clear existing boxes
        
        # Add source square (red)
        if source_square in self.board_coordinates:
            self.add_square(source_square, self.source_color)
        
        # Add target square (green)
        if target_square in self.board_coordinates:
            self.add_square(target_square, self.target_color)
    
    def add_square(self, square, color):
        coords = self.board_coordinates[square]
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        self.add_box(
            x1, y1,
            x2, y2,
            color
        )