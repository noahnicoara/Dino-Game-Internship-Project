"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame
from random import randint

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def display_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = game_font.render(f"Score: {current_time}", False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(egg_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)
        

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []


def player_animation():
    global player_surf, player_index
    # Play walking animations if player is on the floor
    # Display jump animation when player is not on the floor
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False
start_time = 0
score = 0

# Game state variables
is_playing = False  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -16.7  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
# score_surf = game_font.render("SCORE?", False, "Black")
# score_rect = score_surf.get_rect(center=(400, 50))

# Load sprite assets
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/player_jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
players_gravity_speed = 0

obstacle_rect_list = []

# Obstacles

# Egg 
egg_frame_1 = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_frame_2 = pygame.image.load("graphics/egg/egg_2.png").convert_alpha()

# Fly 
fly_frame_1 = pygame.image.load('graphics/fly/fly_1.png').convert_alpha()
fly_frame_1 = pygame.transform.rotozoom(fly_frame_1,0,3.5)
fly_frame_2 = pygame.image.load('graphics/fly/fly_2.png').convert_alpha()
fly_frame_2 = pygame.transform.rotozoom(fly_frame_2,0,3.5)
# Intro screen
player_stand = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = game_font.render('Dino Game', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = game_font.render('Press space to start', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,340))

# Tiimer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1250)

while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                start_time = int(pygame.time.get_ticks() / 100) 

        if event.type == obstacle_timer and is_playing:
            if randint(0,2):
                obstacle_rect_list.append(egg_surf.get_rect(bottomleft=(randint(900,1100),300)))
            else:
                 obstacle_rect_list.append(fly_surf.get_rect(bottomleft=(randint(900,1100),225)))


    if is_playing:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        # pygame.draw.rect(screen, "#c0e8ec", score_rect)
        # pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        # screen.blit(score_surf, score_rect)
        score = display_score()

        # Adjust egg's horizontal location then blit it
        # egg_rect.x -= 5
        # if egg_rect.right <= 0:
        #     egg_rect.left = 800
        # screen.blit(egg_surf, egg_rect)

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf,player_rect)

        # Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collisions
        is_playing = collisions(player_rect,obstacle_rect_list) 

        # When player collides with enemy, game ends

    # When game is over, display game over message
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        players_gravity_speed = 0
        score_message = game_font.render(f"Your score: {score}", False, (111,196,169))
        score_message_rect = score_message.get_rect( center = (400,330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
