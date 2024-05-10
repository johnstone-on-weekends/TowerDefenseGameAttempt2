import pygame as pg
from pygame.math import Vector2
import math
from enemy_data import ENEMY_DATA
import constants as c


class Enemy(pg.sprite.Sprite):

    def __init__(self, enemy_type, waypoints, images):
        pg.sprite.Sprite.__init__(self)

        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.speed = ENEMY_DATA[enemy_type]["speed"]
        self.health = ENEMY_DATA[enemy_type]["health"]

        self.original_image = images[enemy_type]
        self.angle = 0
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world):
        # Define a target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # Enemy has arrived at target, delete the enemy
            self.kill()
            world.health -= 1
            world.missed_enemies += 1

        # Calculate distance to target
        dist = self.movement.length()

        # Check if remaining distance is greater than the enemy speed
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            # Ensure that we get the dist to 0 and then update the target waypoint
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self):
        # Calculate distance to next waypoint
        dist = self.target - self.pos

        # Use distance to calculate angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))

        # Rotate image and update rectangle
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += 1
            self.kill()

