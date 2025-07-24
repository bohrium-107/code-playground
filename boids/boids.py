import math
import random
import pygame as pg
from pygame import gfxdraw
import globals

class Boid:
    COLOR = pg.color.Color('white')
    WIDTH = 15
    HEIGHT = 25
    START_VEL = 10

    VIEW_RADIUS = 140
    SEPARATION = 8
    ALIGNMENT = 2
    COHESION = 2
    BORDER_REPULSION = 5
    BORDER_TRESHOLD = 90
    MAX_VELOCITY = 50

    def __init__(self):
        self.x = random.randint(0, screen.width)
        self.y = random.randint(0, screen.height)
        self.velx = random.randint(-self.START_VEL, self.START_VEL)
        self.vely = random.randint(-self.START_VEL, self.START_VEL)
        self.angle = 0

        self.orig_surf = pg.Surface((self.HEIGHT, self.WIDTH))
        self.orig_surf.set_colorkey(pg.color.Color('black'))

        # Draw antialiased triangle on orig_surf
        pg.gfxdraw.aatrigon(self.orig_surf, 0, 0, 0, self.WIDTH, self.HEIGHT - 1, self.WIDTH // 2, self.COLOR)
        pg.gfxdraw.filled_trigon(self.orig_surf, 0, 1, 0, self.WIDTH - 1, self.HEIGHT - 2, self.WIDTH // 2, self.COLOR)

    def update(self):
        nearest = list(filter(lambda x: self.distance_to(x) <= self.VIEW_RADIUS, boids))

        direction_sum_x = 0
        direction_sum_y = 0
        sum_x = 0
        sum_y = 0
        accx = 0
        accy = 0

        for other in nearest:
            if other == self:
                continue

            # Compute average direction of neighbors
            other_vel = other.get_velocity()
            if other_vel != 0:
                direction_sum_x += other.velx / other_vel
                direction_sum_y += other.vely / other_vel

            # Compute average position of neighbors
            sum_x += other.x
            sum_y += other.y

            # Add repulsion force from neighbors
            dist_to_other = self.distance_to(other)
            if dist_to_other != 0:
                repulsion_force = self.SEPARATION / self.distance_to(other)
                accx += repulsion_force * ((self.x - other.x) / self.distance_to(other))
                accy += repulsion_force * ((other.y - self.y) / self.distance_to(other))

        if len(nearest) > 1:
            # Add alignment force
            accx += self.ALIGNMENT * direction_sum_x / len(nearest)
            accy += self.ALIGNMENT * direction_sum_y / len(nearest)

            # Add cohesion force
            avg_x = sum_x / len(nearest)
            avg_y = sum_y / len(nearest)
            dist_to_avg = math.sqrt((avg_x - self.x) ** 2 + (avg_y - self.y) ** 2)
            accx += self.COHESION * ((avg_x - self.x) / dist_to_avg)
            accy += self.COHESION * ((self.y - avg_y) / dist_to_avg)

        # Add repulsion force from borders
        if screen.width - self.x < self.BORDER_TRESHOLD:
            accx -= self.BORDER_REPULSION
        elif self.x < self.BORDER_TRESHOLD:
            accx += self.BORDER_REPULSION

        if screen.height - self.y < self.BORDER_TRESHOLD:
            accy += self.BORDER_REPULSION
        elif self.y < self.BORDER_TRESHOLD:
            accy -= self.BORDER_REPULSION

        self.velx += accx
        self.vely += accy

        # Limit the velocity magnitude
        velocity = self.get_velocity()
        if velocity > self.MAX_VELOCITY:
            self.velx = (self.velx / velocity) * self.MAX_VELOCITY
            self.vely = (self.vely / velocity) * self.MAX_VELOCITY

        self.x += self.velx * delta_time
        self.y -= self.vely * delta_time
        self.angle = math.degrees(math.atan2(self.vely, self.velx))

    # Distance between this boid and another
    def distance_to(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def get_velocity(self):
        return math.sqrt(self.velx ** 2 + self.vely ** 2)

    def draw(self):
        # Rotate the surface around its center
        rotated_surf = pg.transform.rotate(self.orig_surf, self.angle)
        new_rect = rotated_surf.get_rect(center=(self.x, self.y))
        screen.blit(rotated_surf, new_rect)

# Setup
pg.init()
pg.display.set_caption('Boids')
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
