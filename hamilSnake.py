from random import choice
from hamilCycles import randHamilCycleCoords as hamiltonianCycle
from aStarForSnake import aStarSearch

def up(x, y):
    return (x, y - 1)
def down(x, y):
    return (x, y + 1)
def left(x, y):
    return (x - 1, y)
def right(x, y):
    return (x + 1, y)
def nextPos(x, y):
    return [up(x, y), down(x, y), left(x, y), right(x, y)]

def dist2(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1])**2

def hamDist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def inBounds(x, y, xMin, yMin, xMax, yMax):
    if x >= xMin and x < xMax and y >= yMin and y < yMax:
        return True
    else:
        return False

class HamiltonianSnake:
    def __init__(self, length, m, n):
        self.m, self.n = m, n
        self.head = (m//2, n//2)
        self.trail = []
        self.cycle = hamiltonianCycle(m, n)
        self.cyclePos = self.cycle.index(self.head)
        self.moveQueue = []
        for i in range(1, length):
            self.trail.append(self.cycle[self.cyclePos - i])
        self.randomiseApple()

    def randomiseApple(self):
        possible = [p for p in self.cycle if p not in self.position()]
        if len(possible) == 0:
            self.apple= (-1, -1)
        else:
            self.apple = choice(possible)
    
    def posInCycle(self, p):
        return self.cycle.index(p)

    def isViable(self, s):
        """
        Decides if s is a viable spot that will not cause the snake to crash

        s should be a position in the cycle not a position in the game board
        """
        if s == (1 + self.cyclePos) % len(self.cycle):
            return True
        elif self.apple == (-1, -1):
            return False
        
        if a == None:
            a = self.posInCycle(self.apple)
        if t == None:
            t = self.posInCycle(self.trail[-1])
        if h == None:
            h = self.cyclePos
        
        a = (a - t) % (self.m * self.n)
        h = (h - t) % (self.m * self.n)
        s = (s - t) % (self.m * self.n)
        t = 0
        if s < h or s > a:
            return False
        else:
            return True
        
    def distToApple(self, p):
        if self.apple == (-1, -1):
            return 0
        possiblePos = self.cycle.index(p)
        appleCyclePos = [*self.cycle[possiblePos:], *self.cycle].index(self.apple)
        return appleCyclePos - possiblePos

    def findPathToApple(self):
        if self.apple != (-1, -1):
            path = aStarSearch(self.position(), self.apple, self.cycle)
        else:
            path = self.cycle[self.cyclePos + 1 : ] + [(0, 0)]
        self.moveQueue.extend(path)

    def move(self):
        if len(self.moveQueue) == 0:
            self.findPathToApple()
            
        newHead = self.moveQueue.pop(0)
        self.trail = [self.head][:] + self.trail
        self.head = newHead
        self.cyclePos = self.posInCycle(self.head)
        if self.head != self.apple:
            self.trail = self.trail[:-1]
        else:
            self.randomiseApple()

    def position(self):
        return [self.head, *self.trail]