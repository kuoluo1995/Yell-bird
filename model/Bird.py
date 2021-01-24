import pygame

from common import *


class Bird:
    """定义一个鸟类"""

    def __init__(self):
        """定义初始化方法"""
        self.bird_rect = pygame.Rect(*BIRD_SIZE)
        self.bird_status = [pygame.image.load('assets/images/bird_stand.png'),
                            pygame.image.load('assets/images/bird_fly.png'),
                            pygame.image.load('assets/images/bird_dead.png')]  # 定义鸟的3种状态列表
        self.is_jump = False  # 默认情况小鸟自动降落
        self.jump_speed = INIT_JUMP_SPEED
        self.gravity = INIT_GRAVITY
        self.is_dead = False  # 默认小鸟生命状态为活着
        self.status = 0
        self.bird_x = BIRD_X
        self.bird_y = BIRD_Y

    def jump(self, volume):
        self.jump_speed = volume // 20
        self.status = 1

    def update(self):
        if self.is_jump and not self.is_dead:  # 小鸟跳跃
            self.jump_speed -= RESISTANCE
            self.bird_y -= self.jump_speed  # 鸟Y轴坐标减小，小鸟上升
        else:  # 小鸟坠落
            self.gravity += ACCELERATION_GRAVITY
            self.bird_y += self.gravity  # 鸟Y轴坐标增加，小鸟下降
        self.bird_rect[1] = self.bird_y  # 更改Y轴位置

    def check_dead(self, up_pipeline, down_pipeline):
        # 检测小鸟与上下方管子是否碰撞
        if up_pipeline.colliderect(self.bird_rect) or down_pipeline.colliderect(self.bird_rect):
            self.is_dead = True
            self.status = 2
        # 检测小鸟是否飞出上下边界
        if not 0 < self.bird_rect[1] < VIEW_HEIGHT:
            self.is_dead = True
            self.status = 2
            return True
        else:
            return False
