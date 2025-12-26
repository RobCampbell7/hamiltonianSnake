# Runs the hamiltonian snake with specified parameters
import pygame
from pygame.locals import *
from hamilSnake import HamiltonianSnake
from time import time

squareSize = 30
boardDim = (20, 20)
moveTime = 0.1

backgroundColour = (25, 25, 25)
appleColour = (200, 200, 200)
snakeColour = (0, 150, 0)

pygame.init()
screen = pygame.display.set_mode((boardDim[0] * squareSize, boardDim[1] * squareSize))
screen.fill((50, 50, 50))

snake = HamiltonianSnake(3, *boardDim)

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
            left = min(snakeBody[i], snakeBody[i - 1], key = lambda p : p[0])[0] * (squareSize) + 1
            top = min(snakeBody[i], snakeBody[i - 1], key = lambda p : p[1])[1] * (squareSize) + 1
            if snakeBody[i][0] == snakeBody[i - 1][0]:
                width = (squareSize) - 2
                height = (squareSize) * 2 - 2
            elif snakeBody[i][1] == snakeBody[i - 1][1]:
                width = (squareSize) * 2 - 2
                height = (squareSize) - 2

            pygame.draw.rect(screen,
                            snakeColour,
                            pygame.Rect(left, top, width, height))
        pygame.draw.rect(screen, appleColour, pygame.Rect(snake.apple[0] * squareSize + 1,
                                                          snake.apple[1] * squareSize + 1,
                                                          squareSize - 2, squareSize - 2))
        pygame.display.flip()