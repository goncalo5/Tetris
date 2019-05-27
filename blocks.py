#!/usr/bin/env python
import pygame as pg
from random import randint
from settings import GAME, SCREEN, BLOCKS, GREEN
vec = pg.math.Vector2


############################################################
# Blocks:

def create_new_block(all_sprites, all_blocks):
    block = pg.sprite.Sprite()
    block.pos = vec((SCREEN['WIDTH'] / 2) * GAME['UNIT'], 0)
    block.vel = vec(0, 0)
    block.image = pg.Surface((GAME['UNIT'], randint(1, 4) * GAME['UNIT']))
    block.image.fill(GREEN)
    block.rect = block.image.get_rect()
    block.rect.x = (SCREEN['WIDTH'] / 2) * GAME['UNIT']
    block.stop = False
    block.can_move_left = True
    block.can_move_right = True

    block.update_time = pg.time.get_ticks()
    block.time_to_press = pg.time.get_ticks()
    all_sprites.add(block)
    all_blocks.add(block)

    return block


def events(block):
    keys = pg.key.get_pressed()

    if not block.stop:
        if keys[pg.K_LEFT] and block.can_move_left:
            block.vel.x += -BLOCKS['VELX']
        if keys[pg.K_RIGHT] and block.can_move_right:
            block.vel.x += BLOCKS['VELX']
        if keys[pg.K_DOWN]:
            block.vel.y += BLOCKS['VELY']
        if keys[pg.K_SPACE]:
            block

    return block


def update(all_sprites, block, now):
    # Update

    if now - block.time_to_press > BLOCKS['TIME_TO_PRESS']:
        block.time_to_press = now
        block = events(block)

    all_sprites.update()
    if now - block.update_time > BLOCKS['TIME_TO_MOVE']:
        block.update_time = now
        if not block.stop:
            block.pos.y += BLOCKS['VELY']

    block.pos += block.vel
