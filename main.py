import pygame
import sys
# Import the SoundManager instance to initialize sounds early
from game.sound_manager import SOUNDS 
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()
# NOTE: pygame.mixer is initialized inside SoundManager.__init__ for robust setup.

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    while True:
        # Fill the screen background
        SCREEN.fill(BLACK)
        
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # --- Game Over Menu Input ---
            if not engine.game_running and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_3:
                    engine.start_new_game(3)
                elif event.key == pygame.K_5:
                    engine.start_new_game(5)
                elif event.key == pygame.K_7:
                    engine.start_new_game(7)

        # --- Game Logic Update ---
        if engine.game_running:
            engine.handle_input()
            engine.update()
            engine.check_for_winner()
        else:
            engine.handle_input()
        
        # --- Rendering ---
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit()
