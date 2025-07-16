import math
import random
import pygame as pg
from pygame import gfxdraw
import globals

class Boid:
    COLOR = pg.color.Color('white')
    WIDTH = 20
    HEIGHT = 30
    VELOCITY = 20

    def __init__(self):
        self.x = random.randint(0, screen.width)
        self.y = random.randint(0, screen.height)
        self.angle = random.randint(0, 359)

        self.orig_surf = pg.Surface((self.HEIGHT, self.WIDTH))
        self.orig_surf.set_colorkey(pg.color.Color('black'))

        # Draw antialiased triangle on orig_surf
        pg.gfxdraw.aatrigon(self.orig_surf, 0, 0, 0, self.WIDTH, self.HEIGHT - 1, self.WIDTH // 2, self.COLOR)
        pg.gfxdraw.filled_trigon(self.orig_surf, 0, 1, 0, self.WIDTH - 1, self.HEIGHT - 2, self.WIDTH // 2, self.COLOR)

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.VELOCITY * delta_time
        self.y -= math.sin(math.radians(self.angle)) * self.VELOCITY * delta_time

    def draw(self):
        # Rotate the surface around its center
        rotated_surf = pg.transform.rotate(self.orig_surf, self.angle)
        new_rect = rotated_surf.get_rect(center=(self.x, self.y))
        screen.blit(rotated_surf, new_rect)

# Setup
pg.init()
screen = pg.display.set_mode((900, 700))
running = True
delta_time = 0.1
clock = pg.time.Clock()

boids = [Boid()]

while running:
    screen.fill(globals.bg_color)

    for boid in boids:
        boid.update()
        boid.draw()

    pg.display.flip()

    delta_time = clock.tick(60) / 100
    delta_time = min(1.0, delta_time)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                boids.clear()
                boids.append(Boid())

pg.quit()
