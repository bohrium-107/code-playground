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
    NEAREST_COUNT = 5
    REPULSION = 20

    def __init__(self):
        self.x = random.randint(0, screen.width)
        self.y = random.randint(0, screen.height)
        self.velx = random.randint(-self.VELOCITY, self.VELOCITY)
        self.vely = random.randint(-self.VELOCITY, self.VELOCITY)
        self.accx = 0
        self.accy = 0
        self.angle = 0

        self.orig_surf = pg.Surface((self.HEIGHT, self.WIDTH))
        self.orig_surf.set_colorkey(pg.color.Color('black'))

        # Draw antialiased triangle on orig_surf
        pg.gfxdraw.aatrigon(self.orig_surf, 0, 0, 0, self.WIDTH, self.HEIGHT - 1, self.WIDTH // 2, self.COLOR)
        pg.gfxdraw.filled_trigon(self.orig_surf, 0, 1, 0, self.WIDTH - 1, self.HEIGHT - 2, self.WIDTH // 2, self.COLOR)

    def update(self):
        nearest = sorted(boids, key=self.distance_to)[:self.NEAREST_COUNT]

        for b in nearest:
            if self.distance_to(b) == 0:
                continue

            repulsion_force = self.REPULSION * 10000 / self.distance_to(b)
            angle_to_b = math.atan2((b.y - self.y), -(b.x - self.x))

            self.accx = repulsion_force * math.cos(angle_to_b)
            self.accy = repulsion_force * math.sin(angle_to_b)

        self.velx += self.accx * delta_time
        self.vely += self.accy * delta_time
        self.x += self.velx * delta_time
        self.y -= self.vely * delta_time
        self.angle = math.degrees(math.atan2(self.vely, self.velx))

    # Distance between this boid and another (squared)
    def distance_to(self, other):
        return (other.x - self.x) ** 2 + (other.y - self.y) ** 2

    def draw(self):
        # Rotate the surface around its center
        rotated_surf = pg.transform.rotate(self.orig_surf, self.angle)
        new_rect = rotated_surf.get_rect(center=(self.x, self.y))
        screen.blit(rotated_surf, new_rect)

# Setup
pg.init()
screen = pg.display.set_mode((1000, 800))
running = True
delta_time = 0.1
clock = pg.time.Clock()

COUNT = 50
boids = [Boid() for _ in range(COUNT)]

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
                boids = [Boid() for _ in range(COUNT)]

pg.quit()
