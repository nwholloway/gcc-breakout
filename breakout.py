import sys
import pygame


def game_init():
    """
    Perform global initialisation
    """
    global screen, clock
    global arena
    global ball_image

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
    global screen
    global ball_image, ball_position, ball_direction

    ball_position = ball_image.get_rect()
    ball_position.center = (screen.get_width() / 2, 200)

    ball_direction = [-1, 1]


def game_input():
    """
    Handle input
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def game_update():
    """
    Update the game state
    """
    global clock
    global arena
    global ball_position, ball_direction

    # Milliseconds used in previous tick
    tick = clock.get_time()

    # Update the position of the ball, ensuring it doesn't move out of game arena
    ball_position.x += ball_direction[0] * tick // 5
    ball_position.y += ball_direction[1] * tick // 5
    ball_position.clamp_ip(arena)

    # If the ball hits the edge of the arena, bounce off
    if ball_position.left == arena.left or ball_position.right == arena.right:
        ball_direction[0] *= -1
    if ball_position.top == arena.top or ball_position.bottom == arena.bottom:
        ball_direction[1] *= -1


def game_draw():
    # Display the game state

    global screen, arena
    global ball_image, ball_position

    # Clear the screen
    screen.fill([127, 127, 127])

    # Draw the arena
    pygame.draw.rect(screen, [0, 0, 0], arena)

    # Draw the ball
    screen.blit(ball_image, ball_position)

    # Update the display to the screen
    pygame.display.flip()

    # Delay until time for next frame
    clock.tick(50)


if __name__ == "__main__":
    game_init()
    game_run()
