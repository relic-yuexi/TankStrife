import pygame
import sys
import math

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
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)


# 坦克类
class Tank:
    def __init__(self, x, y, color, control_keys):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 3
        self.size = 40
        self.angle = 0
        self.control_keys = control_keys

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(0, min(self.x, WIDTH - self.size))
        self.y = max(0, min(self.y, HEIGHT - self.size))
        if dx != 0 or dy != 0:
            self.angle = math.atan2(dy, dx)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        end_x = self.x + self.size / 2 + math.cos(self.angle) * self.size
        end_y = self.y + self.size / 2 + math.sin(self.angle) * self.size
        pygame.draw.line(
            screen,
            BLACK,
            (self.x + self.size / 2, self.y + self.size / 2),
            (end_x, end_y),
            5,
        )

    def fire(self):
        return Bullet(
            self.x + self.size / 2, self.y + self.size / 2, self.angle, self.color
        )


# 子弹类
class Bullet:
    def __init__(self, x, y, angle, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 7
        self.color = color

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)


# 障碍物类
class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)


# 创建坦克
tank1 = Tank(
    100,
    HEIGHT // 2,
    GREEN,
    {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d,
        "fire": pygame.K_f,
    },
)
tank2 = Tank(
    WIDTH - 140,
    HEIGHT // 2,
    BLUE,
    {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "fire": pygame.K_SPACE,
    },
)

# 创建障碍物
obstacles = [
    Obstacle(WIDTH // 2 - 25, HEIGHT // 2 - 100, 50, 200),
    Obstacle(200, 100, 50, 50),
    Obstacle(WIDTH - 250, HEIGHT - 150, 50, 50),
]

bullets = []

# 游戏主循环
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == tank1.control_keys["fire"]:
                bullets.append(tank1.fire())
            elif event.key == tank2.control_keys["fire"]:
                bullets.append(tank2.fire())

    # 移动坦克
    for tank in [tank1, tank2]:
        keys = pygame.key.get_pressed()
        dx = keys[tank.control_keys["right"]] - keys[tank.control_keys["left"]]
        dy = keys[tank.control_keys["down"]] - keys[tank.control_keys["up"]]
        tank.move(dx, dy)

    # 移动子弹
    for bullet in bullets[:]:
        bullet.move()
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)

    # 绘制
    screen.fill(WHITE)
    for obstacle in obstacles:
        obstacle.draw()
    tank1.draw()
    tank2.draw()
    for bullet in bullets:
        bullet.draw()
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)
