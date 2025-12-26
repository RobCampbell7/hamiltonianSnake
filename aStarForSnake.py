from math import inf
from random import choice, randint
from hamilCycles import randHamilCycleCoords

class Node:
    def __init__(self):
        # self.body = []
        self.f = inf
        self.g = inf
        self.h = inf
        self.parentI = None
        self.parentJ = None

def hamDist(pos, dest):
    return abs(pos[0] - dest[0]) + abs(pos[1] - dest[1])

def insert(item, lst, key=lambda x : x, asc=True):
    for i in range(len(lst)):
        if key(lst[i]) > key(item) and asc == True or key(lst[i]) < key(item) and asc == False:
            return lst[:i] + [item] + lst[i:]
    return lst + [item]

def neighbours(p):
    return [
        (p[0] + 1, p[1]    ),
        (p[0]    , p[1] + 1),
        (p[0] - 1, p[1]    ),
        (p[0]    , p[1] - 1)
    ]

def inBounds(i, j, m, n):
    if i < 0 or j < 0:
        return False
    elif j >= m or i >= n:
        return False
    else:
        return True

def isAllowed(i, j, body, apple, cycle, m, n):
    if i >= m or i < 0 or j >= n or j < 0:
        return False
    s = cycle.index((i, j))
    h = cycle.index(body[0])
    a = cycle.index(apple)
    t = cycle.index(body[-1])

    a = (a - t) % (m * n)
    h = (h - t) % (m * n)
    s = (s - t) % (m * n)
    t = 0
    if s < h or s > a:
        return False
    else:
        return True
    
def tracePath(nodes, src, dest):
    path = []
    i, j = dest
    while i != None and j != None:
        path = [(i, j)] + path
        i, j = nodes[j][i].parentI, nodes[j][i].parentJ

    return path[1:]

def printSnake(body, apple, m, n):
    output = " "
    for j in range(n):
        for i in range(m):
            if (i, j) in body:
                output += str(body.index((i, j)) + 1) + " "
            elif (i, j) == apple:
                output += "X "
            else:
                output += ". "
        output += "\n "
    print(output)

def aStarSearch(snakeBody, apple, cycle):
    m = max([p[0] for p in cycle]) + 1
    n = max([p[1] for p in cycle]) + 1

    visited = [[False for i in range(m)] for j in range(n)]
    nodes = [[Node() for i in range(m)] for j in range(n)]

    initialMoves = []
    headIndex = cycle.index(snakeBody[0])
    while isAllowed(*apple, snakeBody, apple, cycle, m, n) == False:
        headIndex = (headIndex + 1) % len(cycle)
        initialMoves.append(cycle[headIndex])
        snakeBody = [cycle[headIndex]] + snakeBody[:-1]

    visited = [[False for i in range(m)] for j in range(n)]
    nodes = [[Node() for i in range(m)] for j in range(n)]
    i, j = snakeBody[0]
    nodes[j][i].f = 0
    nodes[j][i].g = 0
    nodes[j][i].h = 0

    heap = [(0, snakeBody[:])]
    found = False
    while len(heap) > 0:
        p = heap.pop(0)
        body = p[1]
        i, j = body[0]
        visited[j][i] = True
        nbours = neighbours((i, j))
        for i2, j2 in nbours:
            if isAllowed(i2, j2, body, apple, cycle, m, n) and visited[j2][i2] == False and (i2, j2) not in body:
                if isAllowed(*apple, [(i2, j2)] + body[:-1], apple, cycle, m, n):
                    nodes[j2][i2].parentI = i
                    nodes[j2][i2].parentJ = j
                    found = True
                    snakeBody = [(i2, j2)] + body[:-1]
                    initialMoves = tracePath(nodes, snakeBody[0], apple)
                else:
                    g2 = nodes[j][i].g + 1
                    h2 = hamDist((i2, j2), apple)
                    f2 = g2 + h2
                    if nodes[j2][i2].f > f2:
                        heap = insert((f2, [(i2, j2)] + body[:-1]), heap, key=lambda x : x[0])
                        nodes[j2][i2].f = f2
                        nodes[j2][i2].g = g2
                        nodes[j2][i2].h = h2
                        nodes[j2][i2].parentI = i
                        nodes[j2][i2].parentJ = j
    
    visited = [[False for i in range(m)] for j in range(n)]
    nodes = [[Node() for i in range(m)] for j in range(n)]
    i, j = snakeBody[0]
    nodes[j][i].f = 0
    nodes[j][i].g = 0
    nodes[j][i].h = 0

    heap = [(0, snakeBody[:])]
    found = False
    while len(heap) > 0:
        p = heap.pop(0)
        body = p[1]
        i, j = body[0]
        visited[j][i] = True
        nbours = neighbours((i, j))
        for i2, j2 in nbours:
            if isAllowed(i2, j2, body, apple, cycle, m, n) and visited[j2][i2] == False and (i2, j2) not in body:
                if (i2, j2) == apple:
                    nodes[j2][i2].parentI = i
                    nodes[j2][i2].parentJ = j
                    found = True
                    return initialMoves + tracePath(nodes, snakeBody[0], apple)
                else:
                    g2 = nodes[j][i].g + 1
                    h2 = hamDist((i2, j2), apple)
                    f2 = g2 + h2
                    if nodes[j2][i2].f > f2:
                        heap = insert((f2, [(i2, j2)] + body[:-1]), heap, key=lambda x : x[0])
                        nodes[j2][i2].f = f2
                        nodes[j2][i2].g = g2
                        nodes[j2][i2].h = h2
                        nodes[j2][i2].parentI = i
                        nodes[j2][i2].parentJ = j
    if found == False:
        return []
