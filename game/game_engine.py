import pygame
from .paddle import Paddle
from .ball import Ball
from .sound_manager import SOUNDS # Import SOUNDS

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.MAX_SCORE = 5 
        
        # Fonts
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 70) 
        self.medium_font = pygame.font.SysFont("Arial", 40)
        
        self.game_running = True
        self.winner = None

    def reset_scores(self):
        """Resets the scores and resets the ball's position and speed."""
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset(reset_speed=True) 

    def start_new_game(self, winning_score):
        """Sets the new winning score target, resets everything, and resumes the game."""
        self.MAX_SCORE = winning_score
        self.game_running = True
        self.winner = None
        self.reset_scores()
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            SOUNDS.SCORE.play() # Play score sound
            self.ball.reset(reset_speed=False) 
        elif self.ball.x >= self.width:
            self.player_score += 1
            SOUNDS.SCORE.play() # Play score sound
            self.ball.reset(reset_speed=False) 

        self.ai.auto_track(self.ball, self.height)

    def check_for_winner(self):
        """Checks if either player has reached the maximum score."""
        if self.player_score >= self.MAX_SCORE or self.ai_score >= self.MAX_SCORE:
            self.game_running = False
            self.winner = "Player" if self.player_score >= self.MAX_SCORE else "AI"

    def render_game_over_menu(self, screen):
        """Renders the game over message and replay menu options."""
        # Winner Message
        winner_message = f"{self.winner} Wins!"
        message_surface = self.big_font.render(winner_message, True, WHITE)
        message_rect = message_surface.get_rect(center=(self.width // 2, self.height // 2 - 100))
        screen.blit(message_surface, message_rect)

        # Replay Options
        menu_title = f"Choose New Game Target (Current: Best of {self.MAX_SCORE})"
        title_surface = self.medium_font.render(menu_title, True, WHITE)
        screen.blit(title_surface, title_surface.get_rect(center=(self.width // 2, self.height // 2)))

        options = [
            ("3", "Best of 3 (Press 3)"),
            ("5", "Best of 5 (Press 5)"),
            ("7", "Best of 7 (Press 7)"),
            ("ESC", "Exit (Press ESC)")
        ]
        
        y_offset = self.height // 2 + 50
        for _, option_text in options:
            option_surface = self.font.render(option_text, True, WHITE)
            screen.blit(option_surface, option_surface.get_rect(center=(self.width // 2, y_offset)))
            y_offset += 40

    def render(self, screen):
        # Draw paddles
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        
        # Draw the center line
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
        
        # Game State Specific Rendering
        if self.game_running:
            # Draw the ball only if the game is active
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        else:
            # If game is over, show the menu
            self.render_game_over_menu(screen)
