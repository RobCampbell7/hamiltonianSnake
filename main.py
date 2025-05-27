import pygame
from pygame.locals import *
from snake import Snake, direction
from time import time

squareSize = 20
boardDim = (20, 20)
moveTime = 0.1
class Square(pygame.sprite.Sprite):
    def __init__(self, colour=(25, 25, 25)):
        super(Square, self).__init__()
        self.surf = pygame.Surface((squareSize - 2, squareSize - 2))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect()

pygame.init()
screen = pygame.display.set_mode((boardDim[0] * squareSize, boardDim[1] * squareSize))
screen.fill((50, 50, 50))

squares = [[Square() for i in range(boardDim[0])] for j in range(boardDim[1])]

snake = Snake(limits=boardDim, length=3)
apple = snake.randomApple()

lastMoveTime = time() - moveTime
stop = False
while stop != True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                stop = True
            elif event.key == K_UP:
                snake.direction = direction.up
            elif event.key == K_DOWN:
                snake.direction = direction.down
            elif event.key == K_LEFT:
                snake.direction = direction.left
            elif event.key == K_RIGHT:
                snake.direction = direction.right
        elif event.type == QUIT:
            stop = True
    
    if time() - lastMoveTime > moveTime:
        lastMoveTime = time()
        snake.move(apple)
        if snake.noApple == True:
            apple = snake.randomApple()
        pos = snake.position()
        
        for j in range(boardDim[1]):
            for i in range(boardDim[0]):
                if (i, j) in pos:
                    squares[i][j].surf.fill((0, 150, 0))
                elif (i, j) == apple:
                    squares[i][j].surf.fill((150, 0, 0))
                else:
                    squares[i][j].surf.fill((25, 25, 25))
                screen.blit(squares[i][j].surf, (1 + squareSize * i, 1 + squareSize * j))
        if snake.isAlive() == False:
            stop = True
        pygame.display.flip()