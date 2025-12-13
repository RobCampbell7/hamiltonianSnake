
# RIGHT lets implement this shit
from random import choice
from hamilCycles import randHamilCycleCoords as hamiltonianCycle

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

    def nextInCycle(self):
        return self.cycle[(1 + self.cyclePos) % len(self.cycle)]
    
    def iterateCycle(self):
        return (1 + self.cyclePos) % len(self.cycle)

    def isViable(self, s, a=None, t=None, h=None):
        if s == self.iterateCycle():
            return True
        elif self.apple == (-1, -1):
            return False
        
        if a == None:
            a = self.posInCycle(self.apple)
        if t == None:
            t = self.posInCycle(self.trail[-1])
        if h == None:
            h = self.cyclePos
        # This is horrendous and messy and im hoping i can simplify it somehow
        if (s <= a and a > h and s > h) or (a < h and (s > h or s <= a)):
            if (h > t and (s > h or s < t)) or (h < t and s > h and s < t):
                return True
        
        return False

    def distToApple(self, p):
        if self.apple == (-1, -1):
            return 0
        possiblePos = self.cycle.index(p)
        appleCyclePos = [*self.cycle[possiblePos:], *self.cycle].index(self.apple)
        return appleCyclePos - possiblePos

    def move(self):
        # newHead = min([p for p in nextPos(*self.head) if self.isViable(self.posInCycle(p))], key=self.distToApple)
        newHead = min([p for p in nextPos(*self.head) if inBounds(*p, 0, 0, self.m, self.n) and self.isViable(self.posInCycle(p))], key=self.distToApple)
        self.trail = [self.head][:] + self.trail
        self.head = newHead
        self.cyclePos = self.posInCycle(self.head)
        if self.head != self.apple:
            self.trail = self.trail[:-1]
        else:
            self.randomiseApple()

    def position(self):
        return [self.head, *self.trail]