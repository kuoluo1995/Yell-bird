import pygame
import sys
import sounddevice as sd
import numpy as np
from common import VIEW_WIDTH, VIEW_HEIGHT, UP_PIPELINE_Y, DOWN_PIPELINE_Y, FONT_FILE, DB
from model.Bird import Bird
from model.Pipeline import Pipeline


def change_volume(indata, outdata, frames, time, status):
    volume = int(np.linalg.norm(indata) * 10)
    game.volume = volume


class Game:
    def __init__(self, bird, up_pipeline, down_pipeline):
        sd.default.device[0] = 1  # 获取麦克风音量
        pygame.init()  # 初始化pygame
        pygame.font.init()  # 初始化字体
        self.font = pygame.font.SysFont(FONT_FILE, 50)  # 设置字体和大小
        self.screen = pygame.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))  # 显示窗口
        self.background = pygame.image.load("assets/images/background.png")  # 加载背景图片
        self.clock = pygame.time.Clock()  # 设置时钟

        self.bird = bird
        self.up_pipeline = up_pipeline
        self.down_pipeline = down_pipeline

        self.score = 0
        self.is_over = True
        self.volume = 0

    def start_game(self):
        with sd.Stream(callback=change_volume):
            while True:
                self.clock.tick(10)  # 每秒执行60次
                ft1_surf = self.font.render('Please Yell', True, (0, 0, 0))  # 设置第一行文字颜色
                self.screen.blit(self.background, (0, 0))  # 填入到背景
                self.screen.blit(ft1_surf, [self.screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # 设置第一行文字显示位置
                ft1_surf = pygame.font.SysFont(FONT_FILE, 30).render('Use Sound to Fly', True, (0, 0, 0))  # 设置第一行文字颜色
                self.screen.blit(ft1_surf, [self.screen.get_width() / 2 - ft1_surf.get_width() / 2, 200])  # 设置第一行文字显示位置
                ft1_surf = pygame.font.SysFont(FONT_FILE, 30).render('When your volume reaches ' + str(DB) + 'DB',
                                                                     True, (242, 3, 36))  # 设置第一行文字颜色
                self.screen.blit(ft1_surf, [self.screen.get_width() / 2 - ft1_surf.get_width() / 2, 300])  # 设置第一行文字显示位置
                ft1_surf = pygame.font.SysFont(FONT_FILE, 30).render('The game will start',
                                                                     True, (242, 3, 36))  # 设置第一行文字颜色
                self.screen.blit(ft1_surf, [self.screen.get_width() / 2 - ft1_surf.get_width() / 2, 350])  # 设置第一行文字显示位置
                ft1_surf = pygame.font.SysFont(FONT_FILE, 30).render('Current volume:' + str(self.volume) + 'DB', True,
                                                                     (242, 3, 36))  # 设置第一行文字颜色
                self.screen.blit(ft1_surf, [self.screen.get_width() / 2 - ft1_surf.get_width() / 2, 400])  # 设置第一行文字显示位置
                pygame.display.flip()
                if self.volume > DB:
                    self.is_over = False
                    self.bird.is_jump = True
                    break
            while True:
                self.clock.tick(15)  # 每秒执行10次
                for event in pygame.event.get():  # 轮询事件
                    if event.type == pygame.QUIT:
                        sys.exit()
                if self.volume > DB and not self.bird.is_dead:
                    self.bird.jump(self.volume)
                if not self.bird.is_dead:
                    self.bird.status = 0
                self.update()

    def update(self):
        self.screen.blit(self.background, (0, 0))  # 填入到背景
        pygame.display.flip()

        up_rect = pygame.Rect(self.up_pipeline.wall_x, self.up_pipeline.wall_y, self.up_pipeline.pine.get_width() - 10,
                              self.up_pipeline.pine.get_height())  # 上方管子的矩形位置

        down_rect = pygame.Rect(self.down_pipeline.wall_x, self.down_pipeline.wall_y,
                                self.down_pipeline.pine.get_width() - 10,
                                self.down_pipeline.pine.get_height())  # 下方管子的矩形位置
        if not self.bird.check_dead(up_rect, down_rect):  # 检测小鸟生命状态
            self.draw_map()  # 创建地图
        else:
            self.game_over()  # 如果小鸟死亡，显示游戏总分数

    def draw_map(self):
        """定义创建地图的方法"""
        # 显示管道
        self.up_pipeline.update()  # 管道移动
        self.score += self.down_pipeline.update()  # 管道移动
        self.screen.blit(self.up_pipeline.pine, self.up_pipeline.size())  # 上管道坐标位置
        self.screen.blit(self.down_pipeline.pine, self.down_pipeline.size())  # 下管道坐标位置
        # 显示小鸟
        self.bird.update()  # 鸟移动
        self.screen.blit(self.bird.bird_status[self.bird.status], (self.bird.bird_x, self.bird.bird_y))  # 设置小鸟的坐标
        # 显示分数
        self.screen.blit(self.font.render('Score:' + str(self.score), True, (0, 0, 0)), (100, 50))  # 设置颜色及坐标位置
        if self.volume > DB:
            color = (242, 3, 36)
        else:
            color = (0, 0, 0)
        ft1_surf = pygame.font.SysFont(FONT_FILE, 30).render('Volume:' + str(self.volume) + 'DB', True, color)
        self.screen.blit(ft1_surf, [250, 60])  # 设置第一行文字显示位置
        pygame.display.update()  # 更新显示

    def game_over(self):
        ft1_surf = self.font.render("Game Over", 1, (242, 3, 36))  # 设置第一行文字颜色
        ft2_surf = self.font.render("Your final score is:  " + str(self.score), 1, (253, 177, 6))  # 设置第二行文字颜色
        self.screen.blit(ft1_surf, [self.screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # 设置第一行文字显示位置
        self.screen.blit(ft2_surf, [self.screen.get_width() / 2 - ft2_surf.get_width() / 2, 200])  # 设置第二行文字显示位置
        pygame.display.flip()  # 更新整个待显示的Surface对象到屏幕上


if __name__ == '__main__':
    """主程序"""
    bird = Bird()
    up_pipeline = Pipeline(UP_PIPELINE_Y, 'assets/images/top_pipeline.png')
    down_pipeline = Pipeline(DOWN_PIPELINE_Y, 'assets/images/down_pipeline.png')
    game = Game(bird, up_pipeline, down_pipeline)
    game.start_game()
    pygame.quit()
