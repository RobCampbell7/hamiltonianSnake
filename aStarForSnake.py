from math import inf
from hamilCycles import randHamilCycleCoords

class Node:
    def __init__(self):
        self.body = []
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

def isValid(i, j, grid):
    if i < 0 or j < 0:
        return False
    elif j >= len(grid) or i >= len(grid[0]):
        return False
    elif grid[j][i] == 1:
        return False
    else:
        return True

def isAllowed(i, j, body, cycle):
    m = max([p[0] for p in cycle])
    n = max([p[1] for p in cycle])

    s = cycle.index((i, j))
    h = cycle.index(body[0])
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

    return [src] + path

def aStarSearch(snakePosition, apple, grid, cycle):
    if snakePosition[0] == apple:
        raise Exception("source and destination are the same")
    elif isValid(*snakePosition[0], grid) == False:
        raise Exception("invalid source")
    elif isValid(*apple, grid) == False:
        raise Exception("invalid source")
    
    visited = [[False for i in range(len(grid[j]))] for j in range(len(grid))]
    nodes = [[Node() for i in range(len(grid[j]))] for j in range(len(grid))]

    i, j = snakePosition[0]
    nodes[j][i].body = snakePosition[:]
    nodes[j][i].f = 0
    nodes[j][i].g = 0
    nodes[j][i].h = 0
    # nodes[j][i].parentI = 0
    # nodes[j][i].parentJ = 0

    heap = [(0, snakePosition)]

    found = False
    while len(heap) > 0:
        p = heap.pop(0)
        i, j = p[1:]
        visited[j][i] = True
        nbours = neighbours((i, j))
        for i2, j2 in nbours:
            newBody = [(i2, j2)] + nodes[i][j].body[:-1]
            if isValid(i2, j2, grid) and visited[j2][i2] == False and isAllowed(i2, j2, newBody, cycle):
                if (i2, j2) == apple:
                    nodes[j2][i2].parentI = i
                    nodes[j2][i2].parentJ = j
                    found = True
                    return tracePath(nodes, snakePosition[0], apple)
                else:
                    g2 = nodes[j][i].g + 1
                    h2 = hamDist((i2, j2), apple)
                    f2 = g2 + h2
                    if nodes[j2][i2].f > f2:
                        heap = insert((f2, i2, j2), heap, key=lambda x : x[0])
                        # print(len(heap))
                        nodes.body = newBody[:]
                        nodes[j2][i2].f = f2
                        nodes[j2][i2].g = g2
                        nodes[j2][i2].h = h2
                        nodes[j2][i2].parentI = i
                        nodes[j2][i2].parentJ = j
    if found == False:
        # raise Exception("No path between source and destiniation")
        return []