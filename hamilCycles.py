from random import choice, randint, shuffle

# cells are numbered row by row on an m wide, n tall grid, so index = y * m + x
def indexToCoord(index, m, n):
    return (index % m, index // m)

def coordToIndex(x, y, m, n):
    return y * m + x

def rotateCycle(cycle, m, n):
    # swap x and y of every cell, for when the cycle was built on the grid the other way round
    newCycle = []
    for i in cycle:
        x, y = indexToCoord(i, m, n)
        newCycle.append(coordToIndex(y, x, n, m))
    
    return newCycle

def hamilCycleIndexes(m, n):
    # the regular cycle: along the whole top row, zigzag down the rows below using columns 1 to m-1,
    # then back up column 0 to the start. the zigzag has to finish next to column 0, which needs an
    # odd number of rows below the top, so n must be even. if only m is even, build it the other way
    # round and rotate the result. a grid with both sides odd has no hamiltonian cycle at all
    rotate = False
    if m % 2 == 1 and n % 2 == 1:
        raise Exception("m or n must have a factor of 2")
    elif m % 2 == 0 and n % 2 == 1:
        rotate = True
        m, n = n, m

    cycle = [*range(m)]
    leftToRight = False
    for row in range(1, n):
        newRow = range(row * m + 1, (row + 1) * m)
        if leftToRight == False:
            newRow = reversed(newRow)

        cycle.extend(newRow)
        leftToRight = not leftToRight

    for row in reversed(range(1, n)):
        cycle.append(row * m)

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

def isCorner(i, c, m, n):
    # true if the i-th cell of the cycle is one of the four grid corners
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
    # consecutive in the cycle, counting the wrap round from the last cell back to the first
    if i not in c or j not in c:
        return False
    
    if i == c[0] and j == c[-1] or j == c[0] and i == c[-1]:
        return True
    if abs(c.index(i) - c.index(j)) == 1:
        return True
    else:
        return False

def printCycle(c, m, n):
    # draws the grid of cell numbers with -- and | between cells that follow each other in the cycle
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
    print(output + "\n\n")

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
    # cuts one cycle into two. pick an edge of the cycle (i1, i2) and a parallel edge (j1, j2)
    # sitting right next to it, then reconnect across the gap so each half closes into its own
    # cycle. corners are skipped because a corner cell only has two neighbours to begin with
    possibleIndexes = [
        i for i in range(m * n)
        if isCorner(i, c, m, n) == False and isCorner((i + 1) % (m * n), c, m, n) == False
    ]
    shuffle(possibleIndexes)

    for iN in possibleIndexes:
        i1 = iN
        i2 = (i1 + 1) % len(c)
        found = False
        for jn in range(m * n):
            if jn not in (i1, i2):
                j1 = jn
                if isCorner(j1, c, m, n) == False and indexesAreNeighbours(c[j1], c[i1], m, n):
                    if isCorner((j1 + 1) % (m * n), c, m, n) == False and indexesAreNeighbours(c[(j1 + 1) % (m * n)], c[i2], m, n) and j1 + 1 not in (i1, i2):
                        j2 = j1 + 1
                        found = True
                        break
                    elif isCorner(j1 - 1, c, m, n) == False and indexesAreNeighbours(c[j1 - 1], c[i2], m, n) and j1 - 1 not in (i1, i2):
                        j2 = j1 - 1
                        found = True
                        break
            

        if found == True:
            break

    # order the four cut points so the i edge comes first in the list, then c1 is the outer part
    # of the list joined across the gap and c2 is the run in the middle
    if j1 < i1:
        i1, i2, j1, j2 = j1, j2, i1, i2
    if i2 > i1:
        i1, i2 = i2, i1
        j1, j2 = j2, j1

    c1 = c[:i2 + 1] + c[j2:]
    c2 = c[i1:j1 + 1]
    return c1, c2

def neighboursPointInCycle(i, c, m, n):
    for j in c:
        if indexesAreNeighbours(i, j, m, n):
            return True
    return False

# rotate a list n places to the right or left
def shiftListR(lst, n):
    if n <= 0:
        return lst
    else:
        return shiftListR([lst[-1], *lst[:-1]], n - 1)
def shiftList(lst, n):
    if n <= 0:
        return lst
    else:
        return shiftList([*lst[1:], lst[0]], n - 1)

def mergeCycles(c1, c2, m, n):
    # joins the two cycles back into one. find an edge of c1 and an edge of c2 that lie side by
    # side, break both, and splice the whole of c2 into c1 between them
    # c1 should be the list starting at zero
    if c1[0] != 0:
        c1, c2 = c2, c1

    # edges of c1 where both ends have a neighbour somewhere in c2
    validNeighbouringIndexes = [
        i for i in range(len(c1)) if neighboursPointInCycle(c1[i], c2, m, n) and neighboursPointInCycle(c1[(i + 1)%len(c1)], c2, m, n)
    ]
    shuffle(validNeighbouringIndexes)

    for i1 in validNeighbouringIndexes:
        i2 = (i1 + 1) % len(c1)
        # i1 and i2 are members of c1
        # j1 and j2 are members of c2
        found = False
        for j in range(len(c2)):
            if indexesAreNeighbours(c1[i1], c2[j], m, n) == True:
                if indexesAreNeighbours(c1[i2], c2[(j + 1)%len(c2)], m, n) == True:
                    j1, j2 = j, j + 1
                    found = True
                    break
                elif indexesAreNeighbours(c1[i2], c2[j - 1], m, n) == True:
                    j1, j2 = j, j - 1
                    found = True
                    break

        if found == True:
            break
    
    if i2 == 0:
        i2 == len(c1)
    if j2 == 0:
        j2 == len(c2)

    # c2 rotated to start at j1 so it enters from c1[i1] and comes back out next to c1[i2]
    c = [
        *c1[0 : i1 + 1],
        *shiftList(c2, j1),
        *c1[i2 :]
    ]
    assert len(c) == m * n
    return c
        
def isValidCycle(c, m, n):
    if len(c) != m * n:
        return False
    for i in range(len(c)):
        if indexesAreNeighbours(c[i - 1], c[i], m, n) == False:
            return False
    return True

def mutateCycle(c, m, n):
    # split and rejoin, which rewires a small patch of the cycle but keeps it hamiltonian
    c1, c2 = splitCycle(c, m, n)
    c = mergeCycles(c1, c2, m, n)
    return c

def randHamilCycleIndexes(m, n):
    # start from the regular cycle and mutate it a number of times to scramble it
    c = hamilCycleIndexes(m, n)
    for i in range(m*n // 2):
        c = mutateCycle(c, m, n)
    return c

def randHamilCycleCoords(m, n):
    c = randHamilCycleIndexes(m, n)
    return [indexToCoord(i, m, n) for i in c]

if __name__ == "__main__":
    m, n = 10, 10
    c = hamilCycleIndexes(m, n)
    assert isValidCycle(c, m, n)
    printCycle(c, m, n)

    
    for i in range(10000):
        c = mutateCycle(c, m, n)
        assert isValidCycle(c, m, n) is True
    
    printCycle(c, m, n)