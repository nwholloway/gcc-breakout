import sys
import pygame


def game_init():
    """
    Perform global initialisation
    """
    global screen, clock
    global arena
    global ball_image
    global paddle_image
    global brick_images

    # Initialise pygame
    pygame.init()

    # Screen
    screen = pygame.display.set_mode((840, 400))

    # The active game area
    arena = pygame.Rect((100, 20), (screen.get_width()-200, screen.get_height()-20))

    # Clock is used to regulate game speed
    clock = pygame.time.Clock()

    # Load images
    ball_image = pygame.image.load("ball.png")
    paddle_image = pygame.image.load("paddle.png")
    brick_images = [pygame.image.load("brick" + str(i) + ".png") for i in [0, 1, 2, 3, 4]]


def game_run():
    """
    Run the game
    """

    game_reset()
    while True:
        game_input()
        game_update()
        game_draw()


def game_reset():
    """
    Initialise the game state
    """
    global screen, arena
    global ball_image, ball_position, ball_direction
    global paddle_image, paddle_position
    global brick_images, brick_positions

    paddle_position = paddle_image.get_rect()
    paddle_position.bottomleft = (arena.left, arena.bottom - 10)

    y = arena.top + 32
    brick_positions = []
    for i, brick_image in enumerate(brick_images):
        brick_positions.append([])
        brick_rect = brick_image.get_rect()
        for x in range(arena.left, arena.right, brick_rect.width):
            brick_position = brick_rect.move(x, y)
            brick_positions[i].append(brick_position)
        y += brick_rect.height

    ball_position = ball_image.get_rect()
    ball_position.midtop = (screen.get_width() / 2, y + 2)

    ball_direction = [-1, 1]


def game_input():
    """
    Handle input
    """
    global keys

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def game_update():
    """
    Update the game state
    """
    global clock
    global keys
    global arena
    global ball_position, ball_direction
    global paddle_position
    global brick_positions

    # Milliseconds used in previous tick
    tick = clock.get_time()

    # Update the position of the ball, ensuring it doesn't move out of game arena
    ball_position.x += ball_direction[0] * tick // 5
    ball_position.y += ball_direction[1] * tick // 5
    ball_position.clamp_ip(arena)

    # Update the position of the paddle, ensuring it doesn't move out of game arena
    if keys[pygame.K_LEFT]:
        paddle_position.x -= tick // 4
    if keys[pygame.K_RIGHT]:
        paddle_position.x += tick // 4
    paddle_position.clamp_ip(arena)

    # If the ball hits a brick, remove it and bounce down
    for brick_line in brick_positions:
        for brick_position in brick_line:
            if ball_position.colliderect(brick_position):
                brick_line.remove(brick_position)
                ball_direction[1] = 1

    # If the ball hits the paddle, bounce up
    if ball_position.colliderect(paddle_position):
        ball_direction[1] = -1

    # If the ball hits the top or sides of the arena, bounce off
    if ball_position.left == arena.left or ball_position.right == arena.right:
        ball_direction[0] *= -1
    if ball_position.top == arena.top:
        ball_direction[1] *= -1

    # If the ball hits the bottom of the arena, reset
    if ball_position.bottom == arena.bottom:
        game_reset()


def game_draw():
    # Display the game state

    global screen, arena
    global ball_image, ball_position
    global paddle_image, paddle_position

    # Clear the screen
    screen.fill([127, 127, 127])

    # Draw the arena
    pygame.draw.rect(screen, [0, 0, 0], arena)

    # Draw the bricks
    for i, brick_image in enumerate(brick_images):
        for brick_position in brick_positions[i]:
            screen.blit(brick_image, brick_position)

    # Draw the paddle
    screen.blit(paddle_image, paddle_position)

    # Draw the ball
    screen.blit(ball_image, ball_position)

    # Update the display to the screen
    pygame.display.flip()

    # Delay until time for next frame
    clock.tick(50)


if __name__ == "__main__":
    game_init()
    game_run()
