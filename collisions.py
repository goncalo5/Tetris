#!/usr/bin/env python
import pygame as pg

from settings import GAME, SCREEN


def stop_the_block(block, stoped_blocks):
    block.stop = True
    stoped_blocks.add(block)
    return block, stoped_blocks


def check_rect_checker(i, stoped_blocks):
    x = GAME['UNIT'] * i
    rect_checker = pg.Rect(x, (SCREEN['HEIGHT'] - 2) * GAME['UNIT'],
                           GAME['UNIT'], GAME['UNIT'])
    for stoped_block in stoped_blocks:
        hit = rect_checker.colliderect(stoped_block.rect)
        if hit:
            return True
    return False


def collision_with_bottom(block, stoped_blocks, destroy1line,
                          floor, all_blocks):
    # collision with other blocks:
    block.rect.y += 1
    hits = pg.sprite.spritecollide(block, stoped_blocks, False)
    if pg.sprite.collide_rect(block, floor) or hits:
        block, stoped_blocks = stop_the_block(block, stoped_blocks)

        n_of_blocks = SCREEN['WIDTH'] - 2
        for i in range(n_of_blocks):
            if not check_rect_checker(i + 1, stoped_blocks):
                break
        else:
            destroy1line = True
            for block in all_blocks:
                block.rect.y += GAME['UNIT']
    block.rect.y -= 1

    return block, stoped_blocks, destroy1line


def collision_with_left(block, stoped_blocks, wall_left):
    block.rect.x -= 1
    hits = pg.sprite.spritecollide(block, stoped_blocks, False) or\
        pg.sprite.collide_rect(block, wall_left)
    if hits:
        block.can_move_left = False
    else:
        block.can_move_left = True
    block.rect.x += 1
    return block


def collision_with_right(block, stoped_blocks, wall_right):
    block.rect.x += 1
    hits = pg.sprite.spritecollide(block, stoped_blocks, False) or\
        pg.sprite.collide_rect(block, wall_right)
    if hits:
        block.can_move_right = False
    else:
        block.can_move_right = True
    block.rect.x -= 1
    return block


def collisions(all_blocks, stoped_blocks, block, destroy1line,
               floor, wall_left, wall_right):
    # collisions:
    block, stoped_blocks, destroy1line =\
        collision_with_bottom(block, stoped_blocks, destroy1line, floor,
                              all_blocks)

    block = collision_with_left(block, stoped_blocks, wall_left)
    block = collision_with_right(block, stoped_blocks, wall_right)
    return all_blocks, stoped_blocks, block, destroy1line
