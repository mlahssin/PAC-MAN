import pygame
from mazegenerator import MazeGenerator


def load_maze(width, height, seed):

    generate = MazeGenerator((width, height), False, seed)

    return generate.maze


print(load_maze(15, 7, 42))
