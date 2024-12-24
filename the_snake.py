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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class EatError (Exception):
    """
    Класс для отслеживания того, укусила ли себя змейка.

    Атрибуты: нет.
    Методы:
        __str__ - сообщение об ошибке.
    """

    def __str__(self):
        """
        Класс для отслеживания укуса себя змейкой.

        Аргументы: нет.
        Возращаемое значение: сообщение об ошибке (str).
        """
        return 'Змейка укусила себя!'


class AppleSnakeError (Exception):
    """
    Класс для отслеживания яблока в змейке.

    Атрибуты: нет.
    Методы:
        __str__ - сообщение об ошибке.
    """

    def __str__(self):
        """
        Класс для отслеживания появления яблока в теле змейки.

        Аргументы: нет.
        Возращаемое значение: сообщение об ошибке (str).
        """
        return 'Яблоко в змейке!'


class GameObject:
    """
    Родительский класс игровых объектов.
    Атрибуты:
        position - позиция объекта.
        body_color - цвет объекта.

    Методы:
        __init__ - инициализация.
        draw - абстрактный метод для отрисовки.
    """

    def __init__(self):
        self.position = ((GRID_WIDTH // 2) * GRID_SIZE,
                         (GRID_HEIGHT // 2) * GRID_SIZE)
        self.body_color = None

    def draw(self):
        """Абстрактный метод для отрисовки."""
        pass


class Apple (GameObject):
    """
    Класс игрового объекта: Яблоко.
    Атрибуты:
        position - позиция объекта.
        body_color - цвет объекта.

    Методы:
        __init__ - инициализация.
        randomize_position - определение новой позиции.
        draw - метод для отрисовки.
    """

    def __init__(self):
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """
        Определяет новую позицию объекта.
        Записывает позицию в аргумент position.

        Аргументы: нет.
        Возвращаемое значение: нет.
        """
        row = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        column = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.position = (column, row)

    def draw(self):
        """
        Отрисовывает объект на игровом поле.

        Аргументы: нет.
        Возвращаемое значение: нет.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake (GameObject):
    """
    Класс игрового объекта: Змея.
    Атрибуты:
        length - количество элементов объекта.
        position - позиции элементов объекта.
        direction - направление движения объекта.
        next_direction - новое направление движения.
        body_color - цвет элементов объекта.

    Методы:
        __init__ - инициализация.
        update_direction - обновляет направление движения.
        move - двигает объект согласно атрибуту direction.
        draw - метод для отрисовки.
        get_head_position - возвращает координаты головы змейки.
        reset - сбрасывает змейку в стартовое состояние.
    """

    def __init__(self):
        self.length = 1
        self.position = ((GRID_WIDTH // 2) * GRID_SIZE,
                         (GRID_HEIGHT // 2) * GRID_SIZE)
        self.positions = [((GRID_WIDTH // 2) * GRID_SIZE,
                           (GRID_HEIGHT // 2) * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """
        Обновляет направление движения змейки
        Записывает новое направление direction
        Сбрасывает next_direction в None

        Аргументы: нет
        Возвращаемое значение: нет
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Перемещает змейку согласно направлению
        Добавляет новый элемент в начало списка positions
        Удаляет последний элемент списка positions

        Аргументы: нет
        Возвращаемое значение: нет
        """
        head = self.get_head_position()
        new_head_col = head[0] + GRID_SIZE * self.direction[0]
        if new_head_col < 0:
            new_head_col = (GRID_WIDTH - 1) * 20
        elif new_head_col > (GRID_WIDTH - 1) * 20:
            new_head_col = 0
        new_head_row = head[1] + GRID_SIZE * self.direction[1]
        if new_head_row < 0:
            new_head_row = (GRID_HEIGHT - 1) * 20
        elif new_head_row > (GRID_HEIGHT - 1) * 20:
            new_head_row = 0
        if (new_head_col, new_head_row) in self.positions[1:]:
            raise EatError
        else:
            self.positions.insert(0, (new_head_col, new_head_row))
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                self.last = None

    def draw(self):
        """
        Отрисовывает змейку

        Аргументы: нет
        Возвращаемое значение: нет
        """
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Возвращает координаты головы змейки

        Аргументы: нет
        Возвращаемое значение: координаты головы (кортеж(int, int))
        """
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает змейку в стартовое состояние

        Аргументы: нет
        Возвращаемое значение: нет
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """
    Определяет нажатую пользователем клавишу
    Изменяет направление движения змейки

    Аргументы:
        game_object - игровой объект (Snake)

    Возвращаемое значение: нет
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
    """Функция main с игрой"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
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
                    try:
                        apple.randomize_position()
                        if apple.position in snake.positions:
                            raise AppleSnakeError
                        break
                    except AppleSnakeError:
                        continue
            snake.move()
        except EatError:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
