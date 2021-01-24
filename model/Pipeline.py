import pygame
import random

from common import PIPELINE_X, PIPELINE_SPEED, PIPELINE_MIN_X, GAME_DIFFICULTY


class Pipeline:
    """定义一个管道类"""

    def __init__(self, wall_y, image):
        """定义初始化方法"""
        self.wall_x = PIPELINE_X
        self.init_y = wall_y
        self.wall_y = wall_y
        self.pine = pygame.image.load(image)

    def size(self):
        return [self.wall_x, self.wall_y]

    def update(self):
        """"管道移动方法"""
        self.wall_x -= PIPELINE_SPEED

        if self.wall_x < PIPELINE_MIN_X:  # 当管道运行到一定位置，即小鸟飞越管道，分数加1，并且重置管道
            self.wall_x = PIPELINE_X
            self.wall_y = self.init_y + random.randint(1, GAME_DIFFICULTY) - GAME_DIFFICULTY//2
            return 1
        return 0
