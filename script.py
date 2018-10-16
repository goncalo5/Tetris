#!/usr/bin/env python
import pygame
import random

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
FPS = 10

# Blocks:
VELX = GAME_UNIT
VELY = GAME_UNIT
TIME_TO_MOVE = 1000


############################################################
# Margins:
def create_margin(pos, sizes):
    margin = pygame.sprite.Sprite()
    margin.image = pygame.Surface(sizes)
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
def create_side(block, which_side):
    # settings:
    side_size = 5
    if which_side in ['left', 'right']:
        width = side_size
        height = GAME_UNIT + 1
        y = - GAME_UNIT - 1
        if which_side == 'left':
            x = block.x - 1
        elif which_side == 'right':
            x = block.x + GAME_UNIT - side_size + 1
            print width, height, x, y
    elif which_side == 'bottom':
        width = GAME_UNIT - 2 * side_size + 2
        height = side_size
        x = block.x + side_size - 1
        y = - side_size
    # logic:
    side = pygame.sprite.Sprite()
    side.image = pygame.Surface((width, height))
    side.image.fill(RED)
    side.rect = side.image.get_rect()
    side.rect.x = x
    side.rect.y = y
    side.dx = block.dx
    side.dy = block.dy
    return block, side


def create_new_block():
    block = pygame.sprite.Group()
    block.x = (WIDTH / 2) * GAME_UNIT
    block.y = 0
    block.dx = 0
    block.dy = VELY
    block.can_move_left = True
    block.can_move_right = True

    # create sides:
    sides = pygame.sprite.Group()
    block, side_left = create_side(block, 'left')
    block, side_right = create_side(block, 'right')
    block, side_bottom = create_side(block, 'bottom')
    sides.add(side_left)
    sides.add(side_right)
    sides.add(side_bottom)
    block.add(sides)
    # all_sprites.add(block)

    # block = pygame.sprite.Sprite()
    # block.image = pygame.Surface((GAME_UNIT, GAME_UNIT))
    # block.image.fill(GREEN)
    # block.rect = block.image.get_rect()
    # block.rect.x = (WIDTH / 2) * GAME_UNIT

    # for unit in block:
    #     unit.x = block.x
    #     unit.y = block.y
    #     unit.dx = block.dx
    #     unit.dy = block.dy
    block.update_time = pygame.time.get_ticks()

    return block, sides, side_left, side_right, side_bottom


def events(event, block):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT and block.can_move_left:
            block.dx = -VELX
        if event.key == pygame.K_RIGHT and block.can_move_right:
            block.dx = VELX
        print 'block.dx', block.dx

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT and block.dx < 0:
            block.dx = 0
        if event.key == pygame.K_RIGHT and block.dx > 0:
            block.dx = 0
    return block


############################################################
# Game:

def quit():
    running = False
    return running


def handle_common_events(event, running, cmd_key_down):
    # check for closing window
    if event.type == pygame.QUIT:
        running = quit()

    if event.type == pygame.KEYDOWN:
        if event.key == 310:
            cmd_key_down = True
        if cmd_key_down and event.key == pygame.K_q:
            running = quit()

    if event.type == pygame.KEYUP:
        if event.key == 310:
            cmd_key_down = False

    return running, cmd_key_down


def run():
    pygame.init()
    pygame.mixer.init()  # for sound
    screen = pygame.display.set_mode((WIDTH * GAME_UNIT, HEIGHT * GAME_UNIT))
    screen.fill(BLACK)
    pygame.display.set_caption(GAME_NAME)

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    margins_with_blocks = pygame.sprite.Group()

    block, sides, side_left, side_right, side_bottom = create_new_block()

    # floor = pygame.sprite.Sprite()
    # floor.image = pygame.Surface((WIDTH * GAME_UNIT, GAME_UNIT))
    # floor.image.fill(BLUE)
    # floor.rect = floor.image.get_rect()
    # floor.rect.x = 0
    # floor.rect.bottom = HEIGHT
    floor, wall_left, wall_right = create_margins()
    margins_with_blocks.add(floor)
    margins_with_blocks.add(wall_left)
    margins_with_blocks.add(wall_right)

    all_sprites.add(floor)
    all_sprites.add(wall_left)
    all_sprites.add(wall_right)
    all_sprites.add(block)

    cmd_key_down = False

    running = True
    while running:
        clock.tick(FPS)

        # Process input (events)
        for event in pygame.event.get():
            running, cmd_key_down = \
                handle_common_events(event, running, cmd_key_down)
            block = events(event, block)

        # Update
        now = pygame.time.get_ticks()
        # hits = pygame.sprite.groupcollide(sides, margins_with_blocks,
        #                                   False, False)
        # print hits

        hit_left = pygame.sprite.spritecollide(side_left, margins_with_blocks,
                                               False)
        # print hit_left
        if hit_left:
            block.can_move_left = False
        else:
            block.can_move_left = True

        hit_right = pygame.sprite.spritecollide(
            side_right, margins_with_blocks, False)
        print hit_right
        if hit_right:
            block.can_move_right = False
        else:
            block.can_move_right = True

        for unit in block:
            unit.rect.x += block.dx
        block.x += block.dx
        # if hits:
        #     for unit in block:
        #         unit.rect.x = unit.oldx
        for unit in block:
            unit.oldx = unit.rect.x

        if now - block.update_time > TIME_TO_MOVE:
            block.update_time = now
            for unit in block:
                #         if not hits:
                unit.rect.x += unit.dx
                unit.rect.y += unit.dy

        all_sprites.update()

        # Render (draw)
        screen.fill(BLACK)
        all_sprites.draw(screen)

        pygame.display.flip()  # always the last

    pygame.quit()


run()
