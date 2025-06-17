from enum import Enum
from random import choice, randint

def move(pos, d):
    match d:
        case direction.up:
            return (pos[0], pos[1] - 1)
        case direction.down:
            return (pos[0], pos[1] + 1)
        case direction.left:
            return (pos[0] - 1, pos[1])
        case direction.right:
            return (pos[0] + 1, pos[1])

def opposite(d):
    match d:
        case direction.up:
            return direction.down
        case direction.down:
            return direction.up
        case direction.left:
            return direction.right
        case direction.right:
            return direction.left

class direction(Enum):
    up = 0
    down = 1
    left = 2
    right = 3

class Snake:
    def __init__(self, start=(-1, -1), limits=(25, 25), length=3, ignoreFirst=True):
        if start == (-1, -1):
            start = (limits[0]//2, limits[1]//2)
        self.head = start
        self.xLim = limits[0] - 1
        self.yLim = limits[1] - 1
        self.direction = direction.right
        self.trail = []
        self.first = ignoreFirst
        self.noApple = True
        for i in range(length - 1):
            if i == 0:
                self.trail.append(move(start, opposite(self.direction)))
            else:
                self.trail.append(move(self.trail[-1], opposite(self.direction)))
    
    def move(self, applePos=(-1, 1)):
        if self.first == False:
            self.trail = [self.head] + self.trail
            self.head = move(self.head, self.direction)
            if self.head != applePos:
                self.trail = self.trail[:-1]
            else:
                self.noApple = True
        else:
            self.first = False

    def position(self):
        return [self.head, *self.trail]

    def isAlive(self):
        if self.head[0] < 0 or self.head[0] > self.xLim:
            return False
        elif self.head[1] < 0 or self.head[1] > self.yLim:
            return False
        elif self.head in self.trail:
            return False
        else:
            return True
    
    def randomApple(self):
        # I would thoroughly like to rewrite this in a more efficient way but im not sure what else
        # to do
        self.noApple = False
        index = randint(0, (1 + self.xLim) * (1 + self.yLim) - len(self.trail) - 1)
        for y in range(self.yLim + 1):
            for x in range(self.xLim + 1):
                if (x, y) not in self.position():
                    if index == 0:
                        return (x, y)
                    else:
                        index -= 1
