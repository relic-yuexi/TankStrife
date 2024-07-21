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
    def __init__(self, center_x, center_y, color, control_keys):
        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.speed = 3
        self.size = 40
        self.angle = 0
        self.control_keys = control_keys
        self.alive = True
        self.barrel_length = 40
        self.rect = pygame.Rect(
            center_x - self.size / 2, center_y - self.size / 2, self.size, self.size
        )

    def move(self, dx, dy, obstacles, other_tank):
        new_x = self.center_x + dx * self.speed
        new_y = self.center_y + dy * self.speed
        new_rect = pygame.Rect(
            new_x - self.size / 2, new_y - self.size / 2, self.size, self.size
        )

        if not self.check_collision(new_rect, obstacles, other_tank):
            self.center_x = new_x
            self.center_y = new_y
            self.rect = new_rect

        self.center_x = max(self.size / 2, min(self.center_x, WIDTH - self.size / 2))
        self.center_y = max(self.size / 2, min(self.center_y, HEIGHT - self.size / 2))
        if dx != 0 or dy != 0:
            self.angle = math.atan2(dy, dx)

    def check_collision(self, new_rect, obstacles, other_tank):
        for obstacle in obstacles:
            if new_rect.colliderect(obstacle.rect):
                return True
        if other_tank.alive and new_rect.colliderect(other_tank.rect):
            return True
        return False

    def draw(self):
        if self.alive:
            x = self.center_x - self.size / 2
            y = self.center_y - self.size / 2
            pygame.draw.rect(screen, self.color, (x, y, self.size, self.size))
            end_x = self.center_x + math.cos(self.angle) * self.barrel_length
            end_y = self.center_y + math.sin(self.angle) * self.barrel_length
            pygame.draw.line(
                screen,
                BLACK,
                (self.center_x, self.center_y),
                (end_x, end_y),
                5,
            )

    def fire(self):
        if self.alive:
            x = self.center_x + self.barrel_length * math.cos(self.angle)
            y = self.center_y + self.barrel_length * math.sin(self.angle)
            return Bullet(x, y, self.angle, self.color)
        return None


# 子弹类
class Bullet:
    def __init__(self, x, y, angle, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 7
        self.color = color
        self.radius = 5

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, obstacles, tanks):
        bullet_rect = pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2
        )
        for obstacle in obstacles:
            if bullet_rect.colliderect(obstacle.rect):
                return True
        for tank in tanks:
            if tank.alive and bullet_rect.colliderect(tank.rect):
                tank.alive = False
                return True
        return False


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
                new_bullet = tank1.fire()
                if new_bullet:
                    bullets.append(new_bullet)
            elif event.key == tank2.control_keys["fire"]:
                new_bullet = tank2.fire()
                if new_bullet:
                    bullets.append(new_bullet)

    # 移动坦克
    for tank in [tank1, tank2]:
        if tank.alive:
            keys = pygame.key.get_pressed()
            dx = keys[tank.control_keys["right"]] - keys[tank.control_keys["left"]]
            dy = keys[tank.control_keys["down"]] - keys[tank.control_keys["up"]]
            other_tank = tank2 if tank == tank1 else tank1
            tank.move(dx, dy, obstacles, other_tank)

    # 移动子弹并检测碰撞
    for bullet in bullets[:]:
        bullet.move()
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)
        elif bullet.check_collision(obstacles, [tank1, tank2]):
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
