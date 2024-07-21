import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置窗口
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Strife")

# 颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


# 坦克类
class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.size = 40

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

        # 确保坦克不会移出屏幕
        self.x = max(0, min(self.x, WIDTH - self.size))
        self.y = max(0, min(self.y, HEIGHT - self.size))

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.size, self.size))


# 创建坦克
tank = Tank(WIDTH // 2, HEIGHT // 2)

# 游戏主循环
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 获取按键状态
    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    # 移动坦克
    tank.move(dx, dy)

    # 绘制
    screen.fill(BLACK)
    tank.draw()
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)
