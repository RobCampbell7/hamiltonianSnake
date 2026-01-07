
class Node:
    def __init__(self, position):
        self.position = position
        self.parent = None
    
    def head(self):
        return self.position[0]
    
    def setParent(self, parentNode):
        self.parent = parentNode

    def tracePath(self):
        if self.parent == None:
            return []
        else:
            return self.parent.tracePath() + [self.head()]

def insert(item, lst, key=lambda x : x, asc=True):
    for i in range(len(lst)):
        if key(lst[i]) > key(item) and asc == True or key(lst[i]) < key(item) and asc == False:
            return lst[:i] + [item] + lst[i:]
    return lst + [item]

def nextSnakes(snakeBody, m, n):
    i, j = snakeBody[0]
    snakes = []
    if i != m - 1 and (i + 1, j) not in snakeBody[:-1]:
        snakes.append(((i + 1, j), (i, j), *snakeBody[1:-1]))
    if j != n - 1 and (i, j + 1) not in snakeBody[:-1]:
        snakes.append(((i, j + 1), (i, j), *snakeBody[1:-1]))
    if i != 0 and (i - 1, j) not in snakeBody[:-1]:
        snakes.append(((i - 1, j), (i, j), *snakeBody[1:-1]))
    if j != 0 and (i, j - 1) not in snakeBody[:-1]:
        snakes.append(((i, j - 1), (i, j), *snakeBody[1:-1]))
    return snakes

def isAllowed(body, cycle, m, n):
    s = cycle.index(body[0])
    h = cycle.index(body[1])
    t = cycle.index(body[-1])

    h = (h - t) % (m * n)
    s = (s - t) % (m * n)
    # t = 0
    if s < h:
        return False
    else:
        return True

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

def pathfind(snakeBody, apple, cycle, m, n):
    if type(snakeBody) != tuple:
        snakeBody = tuple(snakeBody)
    visited = set()
    visited.add(snakeBody)
    nodes = {snakeBody : Node(snakeBody)}

    frontier = [snakeBody]
    found = False
    while len(frontier) > 0 and found == False:
        current = frontier.pop(0)
        visited.add(current)
        for newSnake in nextSnakes(current, m, n):
            if newSnake not in visited and isAllowed(newSnake, cycle, m, n):
                nodes[newSnake] = Node(newSnake)
                nodes[newSnake].setParent(nodes[current])
                if newSnake[0] == apple:
                    found = True
                    return nodes[newSnake].tracePath()
                else:
                    frontier.append(newSnake)
    
    if found == False:
        return [cycle[(cycle.index(snakeBody[0]) + 1) % len(cycle)]]

if __name__=="__main__":
    m, n = 6, 6
    cycle = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0), (3, 0), (3, 1), (4, 1), (4, 0), (5, 0), (5, 1), (5, 2), (5, 3), (4, 3), (4, 2), (3, 2), (2, 2), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4), (4, 4), (5, 4), (5, 5), (4, 5), (3, 5), (2, 5), (2, 4), (1, 4), (1, 5), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1)]
    position = cycle[3 : 0 : -1]
    apple = (0, 4)

    path = pathfind(position, apple, cycle, m, n)
    print(path)
    if len(path) == 0:
        raise Exception