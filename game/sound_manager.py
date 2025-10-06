import pygame
import os

# Define file paths for sound effects (You must provide these files!)
SOUND_DIR = os.path.join(os.path.dirname(__file__), 'sounds') # Assumes sounds are in a 'sounds' directory next to this file

class SoundManager:
    """Manages the loading and playing of all sound effects."""
    def __init__(self):
        try:
            # Initialize Pygame mixer (often done in pygame.init(), but good practice to ensure)
            pygame.mixer.init()
            
            # Load sounds - using dummy paths.
            # You must place your .wav files in a 'sounds' folder relative to main.py
            self.PADDLE_HIT = pygame.mixer.Sound('hit.wav') 
            self.WALL_BOUNCE = pygame.mixer.Sound('wall.wav')
            self.SCORE = pygame.mixer.Sound('score.wav')
            
            print("Sound effects loaded successfully.")
        except pygame.error as e:
            print(f"Error loading sound effects: {e}. Check if files (hit.wav, wall.wav, score.wav) exist.")
            # Create dummy objects if loading fails to prevent crash
            self.PADDLE_HIT = self._dummy_sound()
            self.WALL_BOUNCE = self._dummy_sound()
            self.SCORE = self._dummy_sound()

    def _dummy_sound(self):
        """Creates a dummy class with a .play() method to prevent crashes if mixer fails."""
        class DummySound:
            def play(self):
                pass
        return DummySound()
    
# Global instance of the SoundManager to be used across modules
SOUNDS = SoundManager()
