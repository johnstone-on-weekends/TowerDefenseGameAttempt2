import pygame as pg
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants as c

# Initialize pygame
pg.init()

# Create clock
clock = pg.time.Clock()

# Create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

# Game variables
placing_turrets = False
selected_turret = None

# Load images
# Map
map_image = pg.image.load("levels/level.png").convert_alpha()
# Turret Sprite Sheet
turret_sheet = pg.image.load("assets/images/turrets/turret_1.png").convert_alpha()
# Individual turret image for mouse cursor
cursor_turret = pg.image.load("assets/images/turrets/cursor_turret.png").convert_alpha()
# Enemies
enemy_image = pg.image.load("assets/images/enemies/enemy_1.png").convert_alpha()
# Buttons
buy_turret_image = pg.image.load("assets/images/buttons/buy_turret.png").convert_alpha()
cancel_image = pg.image.load("assets/images/buttons/cancel.png").convert_alpha()

# Load json data for level
with open("levels/level.tmj") as file:
    world_data = json.load(file)


def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

    # Calculate the sequential number of the tile
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    # Check if that tile is grass
    if world.tile_map[mouse_tile_num] == 7:
        # Check that there isn't already a turret there
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free:
            new_turret = Turret(turret_sheet, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)


def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret


def clear_selection():
    for turret in turret_group:
        turret.selected = False


# Create world
world = World(world_data, map_image)
world.process_data()

# Create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

# Create buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)

# Game Loop
running = True

while running:
    clock.tick(c.FPS)

    #########################
    # UPDATING SECTION
    #########################

    # Update groups
    enemy_group.update()
    turret_group.update(enemy_group)

    # Highlight selected turret
    if selected_turret:
        selected_turret.selected = True

    #########################
    # DRAWING SECTION
    #########################

    # Fill a background
    screen.fill("grey100")

    # Draw level
    world.draw(screen)

    # Draw groups
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    # Draw buttons:
    # Button for placing turrets
    if turret_button.draw(screen):
        placing_turrets = True
    # If placing turrets, then show cancel button as well
    if placing_turrets:
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] < c.SCREEN_WIDTH:
            screen.blit(cursor_turret, cursor_rect)
        if cancel_button.draw(screen):
            placing_turrets = False

    # Event handler
    for event in pg.event.get():
        # Quit program
        if event.type == pg.QUIT:
            running = False

        # Mouse left click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            # Check if mouse is on the game area
            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                # Clear selected turrets
                selected_turret = None
                clear_selection()
                if placing_turrets:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    # Update display
    pg.display.update()

pg.quit()

if __name__ == '__main__':
    pass
