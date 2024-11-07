import pygame
import random


class Bomb():
    def __init__(self, initial_speed, invisible=False, netActivated=False):
        self.name = "Bomb"
        self.initial_speed = initial_speed
        self.speed = initial_speed
        self.width, self.height = 50, 50
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = random.randint(0, WIDTH - self.width)
        self.rect.y = HEIGHT


# Initialize Pygame
pygame.init()

# Set the dimensions of the screen
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomb Game")

# Create an instance of Bomb
bomb = Bomb(initial_speed=5)  # Example initial speed

# Load sprite sheet image
sprite_sheet = pygame.image.load("Images/knife.jpg").convert_alpha()

# Define dimensions of each sprite in the sprite sheet
sprite_width = 1920  # Width of each sprite
sprite_height = 1920  # Height of each sprite
black = (0, 0, 0)
white = (255, 255, 255)

def get_image(sheet, x, y, width, height):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (x, y, width, height))
    return image


bomb_image = get_image(sprite_sheet, 0, 0, sprite_width, sprite_width)
bomb_image = pygame.transform.scale(bomb_image, (25, 25))  # Scale down to match bomb size
bomb_image.set_colorkey((255, 255, 255))

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(white)  # Fill with white

    # Draw the bomb on the screen
    screen.blit(bomb_image, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
