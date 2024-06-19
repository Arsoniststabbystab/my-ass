# Importing any needed modules and pygame
import pygame

import random

# Importing pygame locals
from pygame.locals import (
    K_UP,
    RLEACCEL,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

# Defining a Player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Red_Phoenex_mainsprite.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.speed = 40

# Moving the sprite based on user presses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep the player on the screen

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Creating a nemesis
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("Asteroid Brown.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_HEIGHT + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite and make it disappear passes off the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Initialize pygame

pygame.init()

# Defining the display

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600

bg_img = pygame.image.load("Galaxy_sprite.jpg")

# Creating the screen

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a new enemy

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 100)

# Instantiate sprites

player = Player()

# Creating sprite groups

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the game running

running = True

# Main loop
while running:
    # Look at every event in the game queue
    for event in pygame.event.get():
        # Did the user press a key?
        if event.type == KEYDOWN:
            if event.type == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            # Creating a new enemy >:)
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Getting the set of keys pressed and user input
        pressed_keys = pygame.key.get_pressed()

        # Update the player sprite based on key presses
        player.update(pressed_keys)

        # Update enemies
        enemies.update()

    # Filling the screen

        screen.blit(bg_img, (0,0))

        # Draw all sprites
        for entity in enemies:
            screen.blit(entity.surf, entity.rect)

        
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            running = False

        
        screen.blit(player.surf, player.rect)
        pygame.display.flip()
