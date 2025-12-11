from random import choice, randint, shuffle


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
    dx = abs(i % m - j % m)
    dy = abs(i // m - j // m)
    if dx + dy == 1:
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

# def isCorner(i, c, m, n):
#     if c[i] == 0 or c[i] == m * n - 1 or c[i] == m * (n - 1) or c[i] == m - 1:
#         return True
#     elif abs(c[i - 1] - c[i]) != abs(c[i] - c[(i + 1) % (m * n)]):
#         return True
#     else:
#         return False
def isCorner(i, c, m, n):
    if c[i] == 0 or c[i] == m * n - 1 or c[i] == m * (n - 1) or c[i] == m - 1:
        return True
    else:
        return False

def printGrid(m, n):
    numLength = str(len(str(m * n - 1)))
    output = ""
    for i in range(m * n):
        if i != 0 and i % m == 0:
            output += "\n"
        output += (" {:>" + numLength + "}").format(i)
    print(output)

def areCycleAdjacent(i, j, c):
    if i not in c or j not in c:
        return False
    
    # i = i % len(c)
    # j = j % len(c)
    # print("are {0} and {1} adjacent? ".format(c.index(i), c.index(j)), end = "")
    if i == c[0] and j == c[-1] or j == c[0] and i == c[-1]:
        # print("yes")
        return True
    if abs(c.index(i) - c.index(j)) == 1:
        # print("yes")
        return True
    else:
        # print("no")
        return False

def printCycle(c, m, n):
    numLength = str(len(str(m * n - 1)))
    output = ""
    for i in range(m * n):
        if i != 0 and i % m == 0:
            output += "\n"
            for j in reversed(range(m)):
                t = i - (j + 1)
                b = i - (j + 1) + m
                if areCycleAdjacent(t, b, c):
                    output += ("{:^" + numLength + "}").format("|")
                else:
                    output += ("{:^" + numLength + "}").format(" ")
                
                output += "    "
            output += "\n"

        output += ("{:>" + numLength + "}").format(i)
        if areCycleAdjacent(i, (i + 1) % (m*n), c):
            output += " -- "
        else:
            output += "    "
    print(output + "\n")

def neighbours(i, m, n):
    if i // m > 0:
        yield i - m
    if i % m > 0:
        yield i - 1
    if i % m < m - 1:
        yield i + 1
    if i // m < n - 1:
        yield i + m

def splitCycle(c, m, n):
    possibleIndexes = [i for i in range(m * n) if isCorner(i, c, m, n) == False and isCorner((i + 1) % (m * n), c, m, n) == False]
    shuffle(possibleIndexes)

    for iN in possibleIndexes:
        i1 = iN
        i2 = i1 + 1
        # print(iN)
        # i1 and i2 are sequential points in the cycle that neighbour each other
        # j1 and j2 are two sequential points such that i1 neighbours j1 and i2 neighbours j2
        found = False
        for jn in range(m * n):
            if jn not in (i1, i2):
                j1 = jn
                if isCorner(j1, c, m, n) == False and indexesAreNeighbours(c[j1], c[i1], m, n):
                    if isCorner(j1 + 1, c, m, n) == False and indexesAreNeighbours(c[j1 + 1], c[i2], m, n) and j1 + 1 not in (i1, i2):
                        j2 = j1 + 1
                        found = True
                        break
                    elif isCorner(j1 - 1, c, m, n) == False and indexesAreNeighbours(c[j1 - 1], c[i2], m, n) and j1 - 1 not in (i1, i2):
                        j2 = j1 - 1
                        found = True
                        break
            

        if found == True:
            break

    if j1 < i1:
        i1, i2, j1, j2 = j1, j2, i1, i2
    if i2 > i1:
        i1, i2 = i2, i1
        j1, j2 = j2, j1

    c1 = c[:i2 + 1] + c[j2:]
    c2 = c[i1:j1 + 1]
    return c1, c2

if __name__ == "__main__":
    m, n = 6, 6
    # printGrid(m, n)
    c = hamilCycleIndexes(m, n)
    printCycle(c, m, n)

    # print()
    # printCycle([0, 1], m, n)

    # cycle adjacency test
    # for cycleIndex in range(m * n):
    #     assert areCycleAdjacent(c[cycleIndex], c[(cycleIndex + 1) % (m*n)], c)
    #     assert areCycleAdjacent(c[cycleIndex], c[cycleIndex - 1], c)
    #     assert not all([areCycleAdjacent(c[cycleIndex], c[i], c) for i in range(m * n) if i not in ((cycleIndex + 1) % (m*n), cycleIndex - 1)])
    #     # print(c[cycleIndex], end = ", ")
    # print()
    # printCycle(c, m, n)
    # input()
    c1, c2 = splitCycle(c, m, n)
    print(c1)
    print(c2)
    print("\n")
    printCycle(c1, m, n)
    print("\n")
    printCycle(c2, m, n)
    # for i in range(m * n):
    #     assert i in c
    #     assert indexesAreNeighbours(c[i - 1], c[i], m, n)
    
    # c = hamilCycleCoords(m, n)
    # for i in range(m * n):
    #     x0, y0 = indexToCoord(i, m, n)
    #     assert (x0, y0) in c
    #     assert coordsAreNeighbours(c[i], c[i - 1], m, n)
