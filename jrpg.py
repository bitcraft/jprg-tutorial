import pygame
from pygame.locals import *
from pytmx import load_pygame
import pyscroll
import os.path
from collections import deque
from animation import Animation, remove_animations_of
from pygame.math import Vector2

buffer_size = Vector2(320, 240)


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((16, 18))
        self.rect = self.image.get_rect()
        self.image.fill((255, 255, 255))
        self.position = Vector2((20, 20))
        self.update(0)

    def update(self, dt):
        self.rect.center = round(self.position.x), round(self.position.y)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([int(i) for i in buffer_size * 4])
    pygame.display.set_caption('pygame tutorial')

    buffer = pygame.Surface(buffer_size)

    filename = os.path.join('resources', 'village.tmx')
    data = load_pygame(filename)
    source = pyscroll.TiledMapData(data)
    renderer = pyscroll.BufferedRenderer(source, buffer_size, clamp_camera=True)
    group = pyscroll.PyscrollGroup(map_layer=renderer, default_layer=2)

    hero = Hero()
    group.add(hero)
    animations = pygame.sprite.Group()
    camera_position = Vector2(hero.position)

    clock = pygame.time.Clock()
    frame_times = deque(maxlen=30)

    running = True
    while running:
        dt = clock.tick_busy_loop()
        frame_times.append(dt)
        avg_dt = sum(frame_times) / len(frame_times)

        event = pygame.event.poll()
        while event:
            if event.type == QUIT:
                running = False
                break

            event = pygame.event.poll()

        hero_moved = False
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            hero_moved = True
            hero.position.y -= .15 * avg_dt
        elif pressed[K_DOWN]:
            hero_moved = True
            hero.position.y += .15 * avg_dt

        if pressed[K_LEFT]:
            hero_moved = True
            hero.position.x -= .15 * avg_dt
        elif pressed[K_RIGHT]:
            hero_moved = True
            hero.position.x += .15 * avg_dt

        if hero_moved:
            remove_animations_of(animations, camera_position)
            ani = Animation(x=hero.position.x, y=hero.position.y,
                            duration=200, transition='out_quad')
            ani.start(camera_position)
            animations.add(ani)

        animations.update(avg_dt)
        group.update(avg_dt)
        group.center(camera_position)
        group.draw(buffer)

        pygame.transform.scale(buffer, screen.get_size(), screen)

        pygame.display.flip()
