# Runs the hamiltonian snake with specified parameters
import pygame
from pygame.locals import *
from hamilSnake import HamiltonianSnake
from time import time

squareSize = 40
boardDim = (12, 12)
moveTime = 0.05
gapSize = 0.05 * squareSize

backgroundColour = (25, 25, 25)
appleColour = (200, 200, 200)
snakeColour = (0, 150, 0)

snake = HamiltonianSnake(3, *boardDim)

pygame.init()
screen = pygame.display.set_mode((boardDim[0] * squareSize + 2 * gapSize, boardDim[1] * squareSize + 2 * gapSize))
screen.fill((50, 50, 50))

lastMoveTime = time() - moveTime
stop = False
while stop != True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_BACKSPACE):
            stop = True

    if time() - lastMoveTime > moveTime:
        lastMoveTime = time()
        snake.move()

        snakeBody = snake.position()
        apple = snake.apple
        screen.fill(backgroundColour)
        for i in range(1, len(snakeBody)):
            left = min(snakeBody[i], snakeBody[i - 1], key = lambda p : p[0])[0] * (squareSize) + 2 * gapSize
            top = min(snakeBody[i], snakeBody[i - 1], key = lambda p : p[1])[1] * (squareSize) + 2 * gapSize
            if snakeBody[i][0] == snakeBody[i - 1][0]:
                width = (squareSize) - 2 * gapSize
                height = (squareSize) * 2 - 2 * gapSize
            elif snakeBody[i][1] == snakeBody[i - 1][1]:
                width = (squareSize) * 2 - 2 * gapSize
                height = (squareSize) - 2 * gapSize

            pygame.draw.rect(screen,
                            snakeColour,
                            pygame.Rect(left, top, width, height))
        pygame.draw.rect(screen, appleColour, pygame.Rect(snake.apple[0] * squareSize + 2 * gapSize,
                                                          snake.apple[1] * squareSize + 2 * gapSize,
                                                          squareSize - 2 * gapSize, squareSize - 2 * gapSize))
        pygame.display.flip()