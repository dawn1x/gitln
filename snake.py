import pygame
import random
import sys

# 初始化
pygame.init()

# 设置
WIDTH, HEIGHT = 600, 440
UI_HEIGHT = 40  # 顶部 UI 区域高度
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = (HEIGHT - UI_HEIGHT) // CELL_SIZE

# 颜色 - 白底黑图
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# 难度设置 (速度: FPS)
DIFFICULTIES = {
    '1': ('Easy', 5),
    '2': ('Medium', 10),
    '3': ('Hard', 15)
}

# 设置屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # 穿墙处理 - 从另一端出现
        if new_head[0] < 0:
            new_head = (GRID_WIDTH - 1, new_head[1])
        elif new_head[0] >= GRID_WIDTH:
            new_head = (0, new_head[1])
        elif new_head[1] < 0:
            new_head = (new_head[0], GRID_HEIGHT - 1)
        elif new_head[1] >= GRID_HEIGHT:
            new_head = (new_head[0], 0)

        # 撞到自己检测
        if new_head in self.body:
            return False

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

        return True

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def draw(self):
        for i, segment in enumerate(self.body):
            # 蛇头实心，蛇身空心
            rect = (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE + UI_HEIGHT,
                    CELL_SIZE - 2, CELL_SIZE - 2)
            if i == 0:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect, 1)
                # 内部画一个小方块
                inner_rect = (segment[0] * CELL_SIZE + 5,
                             segment[1] * CELL_SIZE + UI_HEIGHT + 5,
                             CELL_SIZE - 12, CELL_SIZE - 12)
                pygame.draw.rect(screen, BLACK, inner_rect)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize()

    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH - 1),
                        random.randint(0, GRID_HEIGHT - 1))

    def draw(self):
        # 食物画成圆形
        x = self.position[0] * CELL_SIZE + CELL_SIZE // 2
        y = self.position[1] * CELL_SIZE + UI_HEIGHT + CELL_SIZE // 2
        pygame.draw.circle(screen, BLACK, (x, y), CELL_SIZE // 2 - 2)

def draw_text_centered(text, font, y_offset=0):
    surface = font.render(text, True, BLACK)
    return surface, (WIDTH // 2 - surface.get_width() // 2,
                     HEIGHT // 2 - surface.get_height() // 2 + y_offset)

def main():
    font_title = pygame.font.Font(None, 48)
    font_normal = pygame.font.Font(None, 36)

    # 选择难度
    difficulty = None
    while difficulty is None:
        screen.fill(WHITE)

        title_surf, title_pos = draw_text_centered("SNAKE", font_title, -80)
        screen.blit(title_surf, title_pos)

        # 显示难度选项
        for i, (key, (name, speed)) in enumerate(DIFFICULTIES.items()):
            text = f"{key}. {name} (Speed: {speed})"
            text_surf, text_pos = draw_text_centered(text, font_normal, -20 + i * 40)
            screen.blit(text_surf, text_pos)

        hint_surf, hint_pos = draw_text_centered("Press 1/2/3 to select", font_normal, 100)
        screen.blit(hint_surf, hint_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    difficulty = DIFFICULTIES[str(event.key - pygame.K_0)]

    game_speed = difficulty[1]

    # 开始游戏
    snake = Snake()
    food = Food()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        if not snake.move():
            # 游戏结束
            game_over = True
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            snake = Snake()
                            food = Food()
                            score = 0
                            game_over = False
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                            difficulty = DIFFICULTIES[str(event.key - pygame.K_0)]
                            game_speed = difficulty[1]
                            snake = Snake()
                            food = Food()
                            score = 0
                            game_over = False

                screen.fill(WHITE)
                text, pos = draw_text_centered(f"Game Over! Score: {score}", font_normal, -40)
                screen.blit(text, pos)

                text2, pos2 = draw_text_centered("Press R to restart, Q to quit", font_normal, 10)
                screen.blit(text2, pos2)

                text3, pos3 = draw_text_centered("Press 1/2/3 to change difficulty", font_normal, 50)
                screen.blit(text3, pos3)

                pygame.display.flip()

        # 吃食物
        if snake.body[0] == food.position:
            snake.grow = True
            score += 10
            food.randomize()

        screen.fill(WHITE)

        # 画网格线 - 从 UI 区域下方开始
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, UI_HEIGHT), (x, HEIGHT))
        for y in range(UI_HEIGHT, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        # 绘制蛇和食物 - 加上 UI 区域偏移
        snake.draw()
        food.draw()

        # 显示分数和难度 - 放在顶部 UI 区域
        score_text = font_normal.render(f"Score: {score}  Level: {difficulty[0]}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(game_speed)

if __name__ == "__main__":
    main()
