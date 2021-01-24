# Bird
INIT_STATUS = 0  # 鸟的矩形
BIRD_SIZE = [65, 50, 50, 50]  # 小鸟的状态
BIRD_X = 100  # 鸟所在X轴坐标,即是向右飞行的速度
BIRD_Y = 350  # 鸟所在Y轴坐标,即上下飞行高度
INIT_JUMP_SPEED = 10  # 跳跃高度
INIT_GRAVITY = 5  # 重力
RESISTANCE = 1  # # 速度递减，上升越来越慢
ACCELERATION_GRAVITY = 0.2  # 重力递增，下降越来越快

# Pipeline
PIPELINE_X = 400  # 管道所在X轴坐标
UP_PIPELINE_Y = -300  # 上管道坐标位置
DOWN_PIPELINE_Y = 500  # 下管道坐标位置
PIPELINE_SPEED = 50  # 管道X轴坐标递减，即管道向左移动
PIPELINE_MIN_X = -80  # 当管道运行到一定位置，即小鸟飞越管道，分数加1，并且重置管道

# 设置窗口
VIEW_HEIGHT = 650
VIEW_WIDTH = 400
FONT_FILE = 'assets/arial.ttf'

# 游戏相关
DB = 200  # 分贝阈值
GAME_SPEED = 15  # 设置游戏速度
GAME_DIFFICULTY = 100  # 水管随机移动的距离
