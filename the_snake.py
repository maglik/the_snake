"""
Игровой модуль для реализации игры "Змейка".

Модуль включает классы для создания игровых объектов,
их поведения и основного цикла игры.
"""

from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class EatError(Exception):
    """Класс для отслеживания того, укусила ли себя змейка."""

    def __str__(self):
        """Возвращает сообщение об ошибке."""
        return "Змейка укусила себя!"


class AppleSnakeError(Exception):
    """Класс для отслеживания появления яблока внутри змейки."""

    def __str__(self):
        """Возвращает сообщение об ошибке."""
        return "Яблоко в змейке!"


class GameObject:
    """Родительский класс для всех игровых объектов."""

    def __init__(self):
        """Инициализация объекта."""
        self.position = ((GRID_WIDTH // 2) * GRID_SIZE,
                         (GRID_HEIGHT // 2) * GRID_SIZE)
        self.body_color = None

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс игрового объекта: яблоко."""

    def __init__(self):
        """Инициализация яблока с случайной позицией."""
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Определяет новую случайную позицию яблока."""
        row = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        column = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.position = (column, row)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс игрового объекта: змейка."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в заданном направлении."""
        head = self.get_head_position()
        new_head_col = head[0] + GRID_SIZE * self.direction[0]
        new_head_row = head[1] + GRID_SIZE * self.direction[1]

        new_head_col %= SCREEN_WIDTH
        new_head_row %= SCREEN_HEIGHT

        if (new_head_col, new_head_row) in self.positions[1:]:
            raise EatError

        self.positions.insert(0, (new_head_col, new_head_row))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """
    Определяет нажатую клавишу и изменяет направление движения змейки.

    Args:
        game_object (Snake): Объект змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запускает основной цикл игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        try:
            handle_keys(snake)
            snake.update_direction()
            if snake.get_head_position() == apple.position:
                snake.length += 1
                while True:
                    apple.randomize_position()
                    if apple.position not in snake.positions:
                        break
            snake.move()
        except EatError:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()