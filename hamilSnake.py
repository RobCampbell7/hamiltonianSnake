from random import choice
from hamilCycles import randHamilCycleCoords as hamiltonianCycle
from aStarForSnake import aStarSearch
from breadthFirstForSnake import pathfind

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

def buildCycleMap(cycle, m, n):
    # To replace the frequent use of index with a faster implementation
    cycleIndex = {}
    for i in range(m * n):
        cycleIndex[cycle[i]] = i
    
    return cycleIndex

class HamiltonianSnake:
    def __init__(self, length, m, n):
        self.m, self.n = m, n
        self.head = (m//2, n//2)
        self.trail = [left(*self.head), left(*left(*self.head))]
        self.cycle = hamiltonianCycle(m, n)
        self.cycleIndex = buildCycleMap(self.cycle, m, n)
        self.moveQueue = []
        # for i in range(1, length):
        #     self.trail.append(self.cycle[self.cyclePos - i])
        self.randomiseApple()

    def randomiseApple(self):
        possible = [p for p in self.cycle if p not in self.position()]
        if len(possible) == 0:
            self.apple= (-1, -1)
        else:
            self.apple = choice(possible)

    def findPath(self):
        if self.apple != (-1, -1):
            path = pathfind(self.position(), self.apple, self.cycle, self.m, self.n)
            print("position:", self.position())
            print("path:", path)
            # path = aStarSearch(self.position(), self.apple, self.cycle)
            print(path)
        else:
            path = self.cycle[self.cyclePos + 1 : ] + [(0, 0)]
        self.moveQueue.extend(path)

    def move(self):
        if len(self.moveQueue) == 0:
            self.findPath()
            
        newHead = self.moveQueue.pop(0)
        self.trail = [self.head][:] + self.trail
        self.head = newHead
        if self.head != self.apple:
            self.trail = self.trail[:-1]
        else:
            self.randomiseApple()

    def position(self):
        return [self.head, *self.trail]