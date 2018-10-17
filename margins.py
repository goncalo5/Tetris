#!/usr/bin/env python
import pygame as pg
from settings import GAME, SCREEN, BLUE


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
    floor_sizes = (SCREEN['WIDTH'] * GAME['UNIT'], GAME['UNIT'])
    floor_pos = (0, (SCREEN['HEIGHT'] - 1) * GAME['UNIT'])
    floor = create_margin(floor_pos, floor_sizes)

    wall_sizes = (GAME['UNIT'], (SCREEN['HEIGHT'] - 1) * GAME['UNIT'])
    wall_left_pos = (0, 0)
    wall_left = create_margin(wall_left_pos, wall_sizes)
    wall_right_pos = ((SCREEN['WIDTH'] - 1) * GAME['UNIT'], 0)
    wall_right = create_margin(wall_right_pos, wall_sizes)

    return floor, wall_left, wall_right
