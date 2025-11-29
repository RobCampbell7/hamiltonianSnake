def indexToCoord(index, m, n):
    # for an m x n grid
    return (index % m, index // m)

def coordToIndex(x, y, m, n):
    # converts a coord to an index
    return y * m + x

def rotateCycle(cycle, m, n):
    newCycle = []
    for i in cycle:
        x, y = indexToCoord(i, m, n)
        newCycle.append(coordToIndex(y, x, n, m))
    
    return newCycle

def hamilCycleIndexes(m, n):
    rotate = False
    if m % 2 == 1 and n % 2 == 1:
        raise Exception("m or n must have a factor of 2")
    elif m % 2 == 0 and n % 2 == 1:
        rotate = True
        m, n = n, m

    cycle = [*range(m)]
    # print(cycle)
    leftToRight = False
    for row in range(1, n):
        newRow = range(row * m + 1, (row + 1) * m)
        if leftToRight == False:
            newRow = reversed(newRow)

        cycle.extend(newRow)
        # print(list(newRow))
        leftToRight = not leftToRight

    # lastRow = []
    for row in reversed(range(1, n)):
        # lastRow.append(row * m)
        cycle.append(row * m)
    # print(lastRow)

    if rotate == True:
        return rotateCycle(cycle, m, n)
    else:
        return cycle

def hamilCycleCoords(m, n):
    cycle = hamilCycleIndexes(m, n)
    return [indexToCoord(i, m, n) for i in cycle]

def indexesAreNeighbours(i, j, m, n):
    d = abs(i - j)
    if d == 1 or d == m:
        return True
    else:
        return False
    
def coordsAreNeighbours(p0, p1, m, n):
    dy = abs(p1[1] - p0[1])
    dx = abs(p1[0] - p0[0])
    if (dy == 0 and dx == 1) or (dy == 1 and dx == 0):
        return True
    else:
        return False

if __name__ == "__main__":
    m, n = 25, 26

    c = hamilCycleIndexes(m, n)

    for i in range(m * n):
        assert i in c
        assert indexesAreNeighbours(c[i - 1], c[i], m, n)
    
    c = hamilCycleCoords(m, n)
    for i in range(m * n):
        x0, y0 = indexToCoord(i, m, n)
        assert (x0, y0) in c
        assert coordsAreNeighbours(c[i], c[i - 1], m, n)
