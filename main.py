"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame
from random import randint

from operator import itemgetter

score_file = "scores.txt"

def load_scores():
    scores = []

    try:
        file = open(score_file, "r")
        for line in file:
            line = line.strip()
            if "," in line:
                name, score = line.rsplit(",", 1)
                scores.append((name,int(score)))
        file.close()
    except FileNotFoundError:
        pass

    scores.sort(key=itemgetter(1), reverse=True)
    return scores [:5]

def save_score(name, score):
    scores = load_scores()
    scores.append((name, score))
    scores.sort(key=itemgetter(1), reverse=True)
    scores = scores[:5]

    file = open(score_file, "w")
    for name, score in scores:
        file.write(f"{name},{score}\n")
    file.close()

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
            obstacle_rect.x -= int(5+score/80)

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
ground_x = 0
ground_speed = 5
game_speed = int(5 + score / 75)
sky_x = 0
lives = 3
is_invincible = False
invincible_timer = 0
invincible_duration = 90
menu_state = "main"
selected_level = 1
is_entering_name = False
username = ""
last_player = ""
SKY_SURF = None

# Game state variables
is_playing = False  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -22.5 # The speed at which the player jumps
players_gravity_speed = 0 # The current speed at which the player falls

# Load level assets
sky_1 = pygame.image.load("graphics/level/sky.png").convert()
sky_2 = pygame.image.load("graphics/level/desert.png").convert()
sky_3 = pygame.image.load("graphics/level/volcano.png").convert()
SKY_SURF = sky_1
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
heart_surf = pygame.image.load("graphics/level/heart.png").convert_alpha()
heart_surf = pygame.transform.scale_by(heart_surf,2.5)
title_screen = pygame.image.load("graphics/menus/title_screen.png").convert()
title_screen = pygame.transform.scale(title_screen, (800,400))
story_screen = pygame.image.load("graphics/menus/story_screen.png").convert()
story_screen = pygame.transform.scale(story_screen, (800,400))
level_screen = pygame.image.load("graphics/menus/level_screen.png").convert()
level_screen = pygame.transform.scale(level_screen, (800,400))
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
game_font = pygame.font.Font("graphics/fonts/PressStart2P.ttf", 32)
# score_surf = game_font.render("SCORE?", False, "Black")
# score_rect = score_surf.get_rect(center=(400, 50))

# Load sprite assets
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_1 = pygame.transform.scale_by(player_walk_1,2)
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk_2 = pygame.transform.scale_by(player_walk_2,2)
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_jump = pygame.transform.scale_by(player_jump,2)

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
players_gravity_speed = 0

obstacle_rect_list = []

# Obstacles

# Egg 
egg_frame_1 = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_frame_1 = pygame.transform.scale_by(egg_frame_1,1.5)
egg_frame_2 = pygame.image.load("graphics/egg/egg_2.png").convert_alpha()
egg_frame_2 = pygame.transform.scale_by(egg_frame_2,1.5)
egg_frames = [egg_frame_1,egg_frame_2]
egg_frame_index = 0
egg_surf = egg_frames[egg_frame_index]

# Fly 
fly_frame_1 = pygame.image.load('graphics/fly/fly_1.png').convert_alpha()
fly_frame_1 = pygame.transform.scale_by(fly_frame_1,2.5)
fly_frame_2 = pygame.image.load('graphics/fly/fly_2.png').convert_alpha()
fly_frame_2 = pygame.transform.scale_by(fly_frame_2,2.5)
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]
# Intro screen
player_stand = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_stand = pygame.transform.scale_by(player_stand,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = game_font.render('Dino Game', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = game_font.render('Press space to start', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,340))

# Tiimer
obstacle_timer = pygame.USEREVENT + 1
spawn_rate = max(450,1250 - score *4)
pygame.time.set_timer(obstacle_timer,spawn_rate)

egg_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(egg_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer,500)

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
            if event.type == pygame.KEYDOWN:

                if menu_state == "main":

                    if event.key == pygame.K_RETURN:
                        lives = 3
                        is_invincible = False
                        is_playing = True
                        start_time = int(pygame.time.get_ticks() / 100) 

                    elif event.key == pygame.K_k:
                        menu_state = "levels"

                    elif event.key == pygame.K_m:
                        menu_state = "story"

                elif menu_state == "levels":

                    if event.key == pygame.K_ESCAPE:
                        menu_state = "main"

                    elif event.key == pygame.K_1:
                        selected_level = 1
                        SKY_SURF = sky_1
                        menu_state = "main"
                    
                    elif event.key == pygame.K_2:
                        selected_level = 2
                        SKY_SURF = sky_2
                        menu_state = "main"

                    elif event.key == pygame.K_3:
                        selected_level = 3
                        SKY_SURF = sky_3
                        menu_state = "main"
                
                elif menu_state == "story":

                    if event.key == pygame.K_ESCAPE:
                        menu_state = "main"

                elif menu_state == "game_over":

                    if is_entering_name:
                        if event.key == pygame.K_RETURN and username.strip():
                            last_player = username.strip()
                            save_score(last_player, score)
                            is_entering_name = False

                        elif event.key == pygame.K_BACKSPACE:
                            username = username[:-1]

                        elif event.unicode.isprintable() and len(username)<12:
                            username += event.unicode
                    else:
                        if event.key == pygame.K_SPACE:
                            lives = 3
                            is_invincible = False
                            obstacle_rect_list.clear()
                            is_playing = True
                            start_time = int(pygame.time.get_ticks() / 100)
                        
                        elif event.key == pygame.K_ESCAPE:
                            menu_state = "main"                     

        if is_playing:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(egg_surf.get_rect(bottomleft=(randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomleft=(randint(900,1100),200)))
            
            if event.type == egg_animation_timer:
                if egg_frame_index == 0: egg_frame_index = 1
                else: egg_frame_index = 0
                egg_surf = egg_frames[egg_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]



    if is_playing:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        sky_x -= game_speed * 0.3

        if sky_x <= -SKY_SURF.get_width():
            sky_x = 0

        screen.blit(SKY_SURF, (sky_x,0))
        screen.blit(SKY_SURF, (sky_x + SKY_SURF.get_width(), 0))


        ground_x -= game_speed * 1.2

        if ground_x <= -GROUND_SURF.get_width():
            ground_x = 0

        screen.blit(GROUND_SURF, (ground_x, GROUND_Y))
        screen.blit(GROUND_SURF, (ground_x + GROUND_SURF.get_width(), GROUND_Y))
        # pygame.draw.rect(screen, "#c0e8ec", score_rect)
        # pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        # screen.blit(score_surf, score_rect)
        score = display_score()
        for i in range(lives):
            screen.blit(heart_surf, (10 + i * 40, 10))

        # Adjust egg's horizontal location then blit it
        # egg_rect.x -= 5
        # if egg_rect.right <= 0:
        #     egg_rect.left = 800
        # screen.blit(egg_surf, egg_rect)

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1

        if players_gravity_speed > 0:
            players_gravity_speed += score/500
        player_rect.y += players_gravity_speed
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        if not is_invincible or pygame.time.get_ticks() % 200 <100:
            screen.blit(player_surf, player_rect)

        # Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collisions
        if not collisions(player_rect, obstacle_rect_list) and not is_invincible:
            lives -= 1

            is_invincible = True
            invincible_timer = invincible_duration

            obstacle_rect_list.clear()

            if lives <= 0:
                is_playing = False
                menu_state = "game_over"
                is_entering_name = True
                username = ""

        # Invincibility Timer

        if is_invincible:
            invincible_timer -= 1

        if invincible_timer <= 0:
            is_invincible = False


        # When player collides with enemy, game ends

    # When game is over, display game over message
    else:
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        players_gravity_speed = 0

        if menu_state == "main":
            screen.blit(title_screen, (0,0))
        
        elif menu_state == "levels":
            screen.blit(level_screen,(0,0))

        elif menu_state == "story":
            screen.blit(story_screen, (0,0))

        elif menu_state == "game_over":
            screen.fill((25, 30, 25))

            title = game_font.render("GAME OVER", False, "white")
            score_text = game_font.render(f"SCORE: {score}", False, "white")

            screen.blit(title, title.get_rect(center=(400, 60)))
            screen.blit(score_text, score_text.get_rect(center=(400, 120)))

            if is_entering_name:
                 name_text = game_font.render("ENTER NAME:", False, "white")
                 typed_text = game_font.render(username + "|", False, "white")
                 save_text = game_font.render("PRESS ENTER TO SAVE", False, "white")
                 
                 screen.blit(name_text, name_text.get_rect(center=(400, 190)))
                 screen.blit(typed_text, typed_text.get_rect(center=(400, 245)))
                 screen.blit(save_text, save_text.get_rect(center=(400, 320)))

            else:
                leaderboard_title = game_font.render("TOP 5", False, "white")
                screen.blit(leaderboard_title, leaderboard_title.get_rect(center=(400, 165)))

                scores = load_scores()

                for i, (name, saved_score) in enumerate(scores):

                    if name == last_player:
                        color = "yellow"
                    else:
                        color = "white"

                    line = game_font.render(
                         f"{i+1}. {name}  {saved_score}",
                        False,
                        color
                    )

                    screen.blit(line, line.get_rect(center=(400, 210 + i * 30)))

                restart = game_font.render("SPACE - PLAY AGAIN", False, "white")
                menu = game_font.render("ESC - MENU", False, "white")

                screen.blit(restart, restart.get_rect(center=(400, 355)))
                screen.blit(menu, menu.get_rect(center=(400, 385)))

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
