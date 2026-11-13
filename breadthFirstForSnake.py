
# a search node is a whole snake, a tuple of cells with the head first, so two states with the same head but different bodies are kept apart
class Node:
    def __init__(self, position):
        self.position = position
        self.parent = None
    
    def head(self):
        return self.position[0]
    
    def setParent(self, parentNode):
        self.parent = parentNode

    def tracePath(self):
        # walk back up the parents, giving the list of heads from the first move to this one
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
    # the up to four snakes one move on: new head, old head, then the body minus its tail.
    # the tail cell is not blocked because it moves out of the way on the same step
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

def isAllowed(body, cycleMap, m, n):
    # cycle positions of the new head, the old head and the tail
    s = cycleMap[body[0]]
    h = cycleMap[body[1]]
    t = cycleMap[body[-1]]

    # measure from the tail so the wrap round of the cycle does not matter. the move is only
    # allowed if the new head is further along the cycle than the old head, which keeps the whole
    # body in cycle order and so stops the snake ever running into itself
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

def pathfind(snakeBody, apple, cycleMap, m, n):
    # breadth first search over snake states, so the first path found is the fewest moves.
    # states are tuples so they can go in the visited set
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
            if newSnake not in visited and isAllowed(newSnake, cycleMap, m, n):
                nodes[newSnake] = Node(newSnake)
                nodes[newSnake].setParent(nodes[current])
                if newSnake[0] == apple:
                    found = True
                    return nodes[newSnake].tracePath()
                else:
                    frontier.append(newSnake)
    
    if found == False:
        return []

if __name__=="__main__":
    m, n = 6, 6
    cycle = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0), (3, 0), (3, 1), (4, 1), (4, 0), (5, 0), (5, 1), (5, 2), (5, 3), (4, 3), (4, 2), (3, 2), (2, 2), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4), (4, 4), (5, 4), (5, 5), (4, 5), (3, 5), (2, 5), (2, 4), (1, 4), (1, 5), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1)]
    position = cycle[3 : 0 : -1]
    apple = (0, 4)

    path = pathfind(position, apple, cycle, m, n)
    print(path)
    if len(path) == 0:
        raise Exception