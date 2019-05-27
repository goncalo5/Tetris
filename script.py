#!/usr/bin/env python
import pygame as pg
# from random import randint
from settings import GAME, SCREEN, BLACK
import blocks
from margins import create_margins
from collisions import collisions
vec = pg.math.Vector2


############################################################
# Game:

def quit():
    running = False
    return running


def handle_common_events(event, running, cmd_key_down):
    # check for closing window
    if event.type == pg.QUIT:
        running = quit()

    if event.type == pg.KEYDOWN:
        if event.key == 310:
            cmd_key_down = True
        if cmd_key_down and event.key == pg.K_q:
            running = quit()

    if event.type == pg.KEYUP:
        if event.key == 310:
            cmd_key_down = False

    return running, cmd_key_down


def run():
    pg.init()
    pg.mixer.init()  # for sound
    screen = pg.display.set_mode((SCREEN['WIDTH'] * GAME['UNIT'], SCREEN['HEIGHT'] * GAME['UNIT']))
    screen.fill(BLACK)
    pg.display.set_caption(GAME['NAME'])

    clock = pg.time.Clock()

    all_sprites = pg.sprite.Group()
    margins = pg.sprite.Group()
    all_blocks = pg.sprite.Group()
    stoped_blocks = pg.sprite.Group()

    block = blocks.create_new_block(all_sprites, all_blocks)

    floor, wall_left, wall_right = create_margins()
    margins.add(floor)
    margins.add(wall_left)
    margins.add(wall_right)

    all_sprites.add(floor)
    all_sprites.add(wall_left)
    all_sprites.add(wall_right)

    destroy1line = False

    cmd_key_down = False

    running = True
    while running:
        clock.tick(SCREEN['FPS'])
        now = pg.time.get_ticks()
        if block.stop:
            print('block.stop')
            block = blocks.create_new_block(all_sprites, all_blocks)
        destroy1line = False

        block.vel = vec(0, 0)

        ############################################################
        # Process input (events)
        for event in pg.event.get():
            running, cmd_key_down = \
                handle_common_events(event, running, cmd_key_down)

        ############################################################
        # update
        blocks.update(all_sprites, block, now)

        all_blocks, stoped_blocks, block, destroy1line =\
            collisions(all_blocks, stoped_blocks, block, destroy1line,
                       floor, wall_left, wall_right)
        if not destroy1line:
            block.rect.topleft = block.pos
        ############################################################
        # Render (draw)
        screen.fill(BLACK)
        all_blocks.draw(screen)
        margins.draw(screen)
        # pg.draw.rect(screen, (255, 255, 255, 0.1), rect_checker, 2)

        pg.display.flip()  # always the last

    pg.quit()


run()
