import pygame
import random
import math
from game.sound_manager import SOUNDS # Import SOUNDS

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Store base speed values
        self.initial_speed_x = 5
        self.initial_speed_y = 3
        
        # Use stored base speeds for initial velocity
        self.velocity_x = random.choice([-1, 1]) * self.initial_speed_x
        self.velocity_y = random.choice([-1, 1]) * self.initial_speed_y

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Store current y-velocity to detect bounce
        old_velocity_y = self.velocity_y 

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            
        # Check if bounce occurred (velocity_y changed sign)
        if old_velocity_y != self.velocity_y:
            SOUNDS.WALL_BOUNCE.play()

    def check_collision(self, player, ai):
        SPEED_INCREASE_FACTOR = 0.5
        MAX_SPEED = 15
        hit_detected = False

        # Check collision with Player Paddle (left side)
        if self.rect().colliderect(player.rect()):
            self.velocity_x *= -1  # Reverse horizontal direction
            hit_detected = True
            
            # Reposition the ball to fix tunneling by setting it flush against the paddle
            self.x = player.x + player.width 
            
            # Increase the speed magnitude
            current_speed = abs(self.velocity_x)
            new_speed = min(current_speed + SPEED_INCREASE_FACTOR, MAX_SPEED)
            self.velocity_x = math.copysign(new_speed, self.velocity_x)

        # Check collision with AI Paddle (right side)
        elif self.rect().colliderect(ai.rect()):
            self.velocity_x *= -1  # Reverse horizontal direction
            hit_detected = True
            
            # Reposition the ball to fix tunneling by setting it flush against the paddle
            self.x = ai.x - self.width
            
            # Increase the speed magnitude
            current_speed = abs(self.velocity_x)
            new_speed = min(current_speed + SPEED_INCREASE_FACTOR, MAX_SPEED)
            self.velocity_x = math.copysign(new_speed, self.velocity_x)
            
        if hit_detected:
            SOUNDS.PADDLE_HIT.play()

    def reset(self, reset_speed=False):
        """Resets the ball to the center."""
        self.x = self.original_x
        self.y = self.original_y
        
        if reset_speed:
            self.velocity_x = random.choice([-1, 1]) * self.initial_speed_x
        else:
            current_speed = abs(self.velocity_x)
            self.velocity_x = math.copysign(current_speed, self.velocity_x) * -1
        
        self.velocity_y = random.choice([-1, 1]) * self.initial_speed_y

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
