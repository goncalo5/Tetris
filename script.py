#!/usr/bin/env python
import pygame as pg
from random import randint
vec = pg.math.Vector2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game
GAME_NAME = "My Game"
GAME_UNIT = 30

# Screen
WIDTH = 9
HEIGHT = 10
FPS = 60

# Blocks:
VELX = GAME_UNIT
VELY = GAME_UNIT
TIME_TO_MOVE = 1000
TIME_TO_PRESS = 150


############################################################
# Margins:
def create_margin(pos, sizes):
    margin = pg.sprite.Sprite()
    margin.image = pg.Surface(sizes)
    margin.image.fill(BLUE)
    margin.rect = margin.image.get_rect()
    margin.rect.topleft = pos
    return margin


def create_margins():
    floor_sizes = (WIDTH * GAME_UNIT, GAME_UNIT)
    floor_pos = (0, (HEIGHT - 1) * GAME_UNIT)
    floor = create_margin(floor_pos, floor_sizes)

    wall_sizes = (GAME_UNIT, (HEIGHT - 1) * GAME_UNIT)
    wall_left_pos = (0, 0)
    wall_left = create_margin(wall_left_pos, wall_sizes)
    wall_right_pos = ((WIDTH - 1) * GAME_UNIT, 0)
    wall_right = create_margin(wall_right_pos, wall_sizes)

    return floor, wall_left, wall_right


############################################################
# Blocks:

def create_new_block(all_sprites):
    print 'create_new_block'
    block = pg.sprite.Sprite()
    block.pos = vec((WIDTH / 2) * GAME_UNIT, 0)
    block.vel = vec(0, 0)
    block.image = pg.Surface((GAME_UNIT, randint(2, 4) * GAME_UNIT))
    block.image.fill(GREEN)
    block.rect = block.image.get_rect()
    block.rect.x = (WIDTH / 2) * GAME_UNIT
    block.stop = False
    block.can_move_left = True
    block.can_move_right = True

    block.update_time = pg.time.get_ticks()
    block.time_to_press = pg.time.get_ticks()
    all_sprites.add(block)

    return block


def events(block):
    keys = pg.key.get_pressed()

    if not block.stop:
        if keys[pg.K_LEFT] and block.can_move_left:
            block.vel.x += -VELX
        if keys[pg.K_RIGHT] and block.can_move_right:
            block.vel.x += VELX
        if keys[pg.K_DOWN]:
            block.vel.y += VELY
        if keys[pg.K_SPACE]:
            block

    return block


############################################################


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
    screen = pg.display.set_mode((WIDTH * GAME_UNIT, HEIGHT * GAME_UNIT))
    screen.fill(BLACK)
    pg.display.set_caption(GAME_NAME)

    clock = pg.time.Clock()

    all_sprites = pg.sprite.Group()
    margins_with_blocks = pg.sprite.Group()
    stoped_blocks = pg.sprite.Group()

    # block, sides, side_left, side_right, side_bottom = create_new_block()
    block = create_new_block(all_sprites)

    floor, wall_left, wall_right = create_margins()
    margins_with_blocks.add(floor)
    margins_with_blocks.add(wall_left)
    margins_with_blocks.add(wall_right)

    all_sprites.add(floor)
    all_sprites.add(wall_left)
    all_sprites.add(wall_right)

    cmd_key_down = False

    running = True
    while running:
        clock.tick(FPS)
        now = pg.time.get_ticks()
        if block.stop:
            print 'stop'
            block = create_new_block(all_sprites)

        block.vel = vec(0, 0)

        # Process input (events)
        for event in pg.event.get():
            running, cmd_key_down = \
                handle_common_events(event, running, cmd_key_down)

        if now - block.time_to_press > TIME_TO_PRESS:
            block.time_to_press = now
            block = events(block)

        # Update
        all_sprites.update()
        if now - block.update_time > TIME_TO_MOVE:
            block.update_time = now
            if not block.stop:
                block.pos.y += VELY

        block.pos += block.vel

        # collisions:

        def stop_the_block(block, stoped_blocks):
            block.stop = True
            stoped_blocks.add(block)
            return block, stoped_blocks

        # collstion with bottom:
        # collision with other blocks:
        block.rect.y += 1
        hits = pg.sprite.spritecollide(block, stoped_blocks, False)
        if hits:
            block, stoped_blocks = stop_the_block(block, stoped_blocks)
        if pg.sprite.collide_rect(block, floor):
            block, stoped_blocks = stop_the_block(block, stoped_blocks)
        block.rect.y -= 1
        # collstion with left:
        block.rect.x -= 1
        hits = pg.sprite.spritecollide(block, stoped_blocks, False) or\
            pg.sprite.collide_rect(block, wall_left)
        if hits:
            block.can_move_left = False
        else:
            block.can_move_left = True
        block.rect.x += 1
        # collstion with right:
        block.rect.x += 1
        hits = pg.sprite.spritecollide(block, stoped_blocks, False) or\
            pg.sprite.collide_rect(block, wall_right)
        if hits:
            block.can_move_right = False
        else:
            block.can_move_right = True
        block.rect.x -= 1

        block.rect.topleft = block.pos

        # Render (draw)
        screen.fill(BLACK)
        all_sprites.draw(screen)

        pg.display.flip()  # always the last

    pg.quit()


run()
