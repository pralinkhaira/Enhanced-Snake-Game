import turtle
import random

# Constants
WIDTH = 500
HEIGHT = 500
FOOD_SIZE = 10
DELAY = 100

# Game variables
snake = []
snake_direction = "up"
food_pos = (0, 0)
score = 0
level = 1
game_over = False

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

# Obstacles
obstacles = []

# Power-ups
power_ups = []

def reset():
    global snake, snake_direction, food_pos, score, level, game_over
    snake = [[0, 0], [0, 20], [0, 40], [0, 60]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    score = 0
    level = 1
    game_over = False
    pen.clear()
    pen.write(f"Score: {score}  Level: {level}", align="center", font=("Courier", 12, "bold"))
    move_snake()

def move_snake():
    global snake_direction, score, level, game_over

    if game_over:
        return

    #  Next position for head of snake.
    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_direction][0]
    new_head[1] = snake[-1][1] + offsets[snake_direction][1]

    # Check self-collision
    if new_head in snake[:-1] or is_collision(new_head, obstacles):
        game_over = True
        pen.goto(0, 0)
        pen.write("GAME OVER", align="center", font=("Courier", 24, "bold"))
        return

    # Check boundary collision
    if is_collision(new_head, [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2, -HEIGHT // 2),
                               (-WIDTH // 2, HEIGHT // 2), (-WIDTH // 2, -HEIGHT // 2)]):
        game_over = True
        pen.goto(0, 0)
        pen.write("GAME OVER", align="center", font=("Courier", 24, "bold"))
        return

    snake.append(new_head)
    if not food_collision():
        snake.pop(0)

    # Clear previous snake stamps
    pen.clearstamps()

    # Draw snake
    for segment in snake:
        pen.goto(segment[0], segment[1])
        pen.stamp()

    # Draw obstacles
    for obstacle in obstacles:
        pen.goto(obstacle[0], obstacle[1])
        pen.stamp()

    # Draw power-ups
    for power_up in power_ups:
        pen.goto(power_up[0], power_up[1])
        pen.stamp()

    # Refresh screen
    screen.update()

    # Rinse and repeat
    turtle.ontimer(move_snake, DELAY)

def food_collision():
    global food_pos, score, level
    if get_distance(snake[-1], food_pos) < 20:
        score += 1
        if score % 5 == 0:
            level += 1
        pen.clear()
        pen.write(f"Score: {score}  Level: {level}", align="center", font=("Courier", 12, "bold"))
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        return True
    return False

def is_collision(pos, objects):
    for obj in objects:
        if get_distance(pos, obj) < 20:
            return True
    return False

def get_random_food_pos():
    x = random.randint(-WIDTH // 2 + FOOD_SIZE, WIDTH // 2 - FOOD_SIZE)
    y = random.randint(-HEIGHT // 2 + FOOD_SIZE, HEIGHT // 2 - FOOD_SIZE)
    return (x, y)

def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance

def go_up():
    global snake_direction
    if snake_direction != "down":
        snake_direction = "up"

def go_right():
    global snake_direction
    if snake_direction != "left":
        snake_direction = "right"

def go_down():
    global snake_direction
    if snake_direction != "up":
        snake_direction = "down"

def go_left():
    global snake_direction
    if snake_direction != "right":
        snake_direction = "left"

def add_power_up():
    power_up = get_random_food_pos()
    power_ups.append(power_up)
    pen.goto(power_up[0], power_up[1])
    pen.stamp()

def two_player_mode():
    global snake_direction
    if snake_direction == "up":
        snake_direction = "down"
    elif snake_direction == "down":
        snake_direction = "up"
    elif snake_direction == "left":
        snake_direction = "right"
    elif snake_direction == "right":
        snake_direction = "left"

# Screen
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(500, 500)
screen.tracer(0)

# Pen
pen = turtle.Turtle("square")
pen.penup()
pen.color("yellow")
pen.hideturtle()
pen.goto(0, HEIGHT // 2 - 40)
pen.write("Score: 0  Level: 1", align="center", font=("Courier", 12, "bold"))

# Food
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.shapesize(FOOD_SIZE / 20)
food.penup()

# Event handlers
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(two_player_mode, "space")

# Obstacle creation
for _ in range(10):
    obstacle = get_random_food_pos()
    obstacles.append(obstacle)
    pen.goto(obstacle[0], obstacle[1])
    pen.stamp()

# Power-up creation
for _ in range(3):
    add_power_up()

# Let's go
move_snake()
turtle.done()
