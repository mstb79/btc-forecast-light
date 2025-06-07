import curses
import random
import time

# Game settings
BOARD_HEIGHT = 20
BOARD_WIDTH = 40
SPEED = 0.1  # seconds between moves

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

OPPOSITE = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}


def create_food(snake):
    """Create food at a random position not occupied by the snake."""
    while True:
        pos = (
            random.randint(1, BOARD_HEIGHT - 2),
            random.randint(1, BOARD_WIDTH - 2),
        )
        if pos not in snake:
            return pos


def init_screen():
    """Initialize curses screen."""
    screen = curses.initscr()
    curses.curs_set(0)  # Hide cursor
    screen.nodelay(True)  # Non-blocking input
    screen.keypad(True)
    return screen


def draw_board(screen, snake, food, score):
    """Draw the game board."""
    screen.clear()
    # Draw borders
    for x in range(BOARD_WIDTH):
        screen.addch(0, x, '#')
        screen.addch(BOARD_HEIGHT - 1, x, '#')
    for y in range(BOARD_HEIGHT):
        screen.addch(y, 0, '#')
        screen.addch(y, BOARD_WIDTH - 1, '#')

    # Draw food
    screen.addch(food[0], food[1], '*')

    # Draw snake
    head = snake[0]
    screen.addch(head[0], head[1], 'O')
    for y, x in snake[1:]:
        screen.addch(y, x, 'o')

    # Display score
    screen.addstr(BOARD_HEIGHT, 0, f" Score: {score} ")
    screen.refresh()


def update_direction(current_dir, key):
    """Update snake direction based on key input."""
    key_map = {
        curses.KEY_UP: UP,
        curses.KEY_DOWN: DOWN,
        curses.KEY_LEFT: LEFT,
        curses.KEY_RIGHT: RIGHT,
    }
    new_dir = key_map.get(key, current_dir)
    if new_dir == OPPOSITE[current_dir]:
        return current_dir
    return new_dir


def main(screen):
    screen.timeout(int(SPEED * 1000))
    snake = [(BOARD_HEIGHT // 2, BOARD_WIDTH // 2 + i) for i in range(3)]
    direction = LEFT
    food = create_food(snake)
    score = 0

    while True:
        draw_board(screen, snake, food, score)
        key = screen.getch()
        direction = update_direction(direction, key)

        new_head = (
            (snake[0][0] + direction[0]) % BOARD_HEIGHT,
            (snake[0][1] + direction[1]) % BOARD_WIDTH,
        )

        if new_head in snake:
            break  # Collision with self

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = create_food(snake)
        else:
            snake.pop()

        time.sleep(SPEED)

    screen.nodelay(False)
    screen.addstr(BOARD_HEIGHT // 2, BOARD_WIDTH // 2 - 5, "Game Over!")
    screen.addstr(BOARD_HEIGHT // 2 + 1, BOARD_WIDTH // 2 - 7, f"Final Score: {score}")
    screen.addstr(BOARD_HEIGHT // 2 + 3, BOARD_WIDTH // 2 - 10, "Press any key to exit")
    screen.getch()


if __name__ == "__main__":
    curses.wrapper(main)
