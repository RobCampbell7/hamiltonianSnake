from aStarNode import Node

def printGrid(grid, startPos = (-1, -1), endPos = (-1, -1)):
    output = " ■" * (len(grid[0]) + 2) + "\n ■"
    for j in range(len(grid)):
        for i in range(len(grid[j])):
            output += " "
            if (i, j) == startPos:
                output += "0"
            elif (i, j) == endPos:
                output += "X"
            elif grid[j][i] == 0:
                output += "."
            elif grid[j][i] == 1:
                output += "■"
        output += " ■\n ■"
    output +=  " ■" * (len(grid[0]) + 1)
    print(output)

def printGridWithPath(grid, path):
    output = " ■" * (len(grid[0]) + 2) + "\n ■"
    for j in range(len(grid)):
        for i in range(len(grid[j])):
            output += " "
            if (i, j) in path[1:-1]:
                output += "o"
            elif (i, j) == path[0] and (i, j) == path[-1]:
                output += "X"
            elif grid[j][i] == 0:
                output += "."
            elif grid[j][i] == 1:
                output += "■"
        output += " ■\n ■"
    output +=  " ■" * (len(grid[0]) + 1)
    print(output)


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
    
def tracePath(nodes, src, dest):
    path = []
    i, j = dest
    while i != None and j != None:
        path = [(i, j)] + path
        i, j = nodes[j][i].parentI, nodes[j][i].parentJ

    return path

def aStarSearch(src, dest, grid):
    if src == dest:
        raise Exception("source and destination are the same")
    elif isValid(*src, grid) == False:
        raise Exception("invalid source")
    elif isValid(*dest, grid) == False:
        raise Exception("invalid source")
    
    visited = [[False for i in range(len(grid[j]))] for j in range(len(grid))]
    nodes = [[Node() for i in range(len(grid[j]))] for j in range(len(grid))]

    i, j = src[:]
    nodes[j][i].f = 0
    nodes[j][i].g = 0
    nodes[j][i].h = 0
    # nodes[j][i].parentI = 0
    # nodes[j][i].parentJ = 0

    heap = [(0, i, j)]

    found = False
    while len(heap) > 0:
        p = heap.pop(0)
        i, j = p[1:]
        visited[j][i] = True
        nbours = neighbours((i, j))
        for i2, j2 in nbours:
            if isValid(i2, j2, grid) and visited[j2][i2] == False:
                if (i2, j2) == dest:
                    nodes[j2][i2].parentI = i
                    nodes[j2][i2].parentJ = j
                    found = True
                    return tracePath(nodes, src, dest)
                else:
                    g2 = nodes[j][i].g + 1
                    h2 = hamDist((i2, j2), dest)
                    f2 = g2 + h2
                    if nodes[j2][i2].f > f2:
                        heap = insert((f2, i2, j2), heap, key=lambda x : x[0])
                        nodes[j2][i2].f = f2
                        nodes[j2][i2].g = g2
                        nodes[j2][i2].h = h2
                        nodes[j2][i2].parentI = i
                        nodes[j2][i2].parentJ = j
    if found == False:
        return []

if __name__=="__main__":
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
        [0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    ]
    src = (0, 0)
    dest = (1, 2)

    # grid = [
    #     [0, 1, 0, 0],
    #     [0, 1, 0, 0],
    #     [0, 1, 0, 0],
    #     [0, 0, 0, 0],
    # ]
    # src = (0, 0)
    # dest = (3, 3)
    path = aStarSearch(src, dest, grid)
    printGridWithPath(grid, path)