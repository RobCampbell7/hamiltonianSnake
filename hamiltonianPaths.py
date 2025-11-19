
# This is specifically for grid paths
# 
#  0   1   2          0   1---2
#                     |   |   |
#  3   4   5    ->    3---4   5
#                             |
#  6   7   8          6---7---8

from random import choice, randint, sample

def indexToCoord(index, m, n):
    # for an m x n grid
    return (index % m, index // n)

def coordToIndex(x, y, m, n):
    return y * m + x

def randNeighbours(index, m, n):
    return sample(neighbours(index, m, n), 4)

def neighbours(index, m, n):
    x, y = indexToCoord(index, m, n)
    nbours = []
    if x > 0:
        nbours.append(index - 1)
    if x < m - 1:
        nbours.append(index + 1)
    if y > 0:
        nbours.append(index - m)
    if y < n - 1:
        nbours.append(index + m)
    
    return filter(lambda i : indexInBounds(i, m, n), nbours)

def indexInBounds(index, m, n):
    if index < -1 or index >= m*n:
        return False
    else:
        return True

def coordInBounds(x, y, m, n):
    if x < 0 or y < 0:
        return False
    elif x > m - 1 or y > n - 1:
        return False
    else:
        return True

def indexesAreNeighbours(i, j, m, n):
    d = abs(i - j)
    if d == 1 or d == m:
        return True
    else:
        return False

def hamiltonianGridPath(m, n):
    # res, sol = [], []
    res, sol, exploredNB = [], [m * n - 1], []
    originNeighbours = neighbours(sol[0])
    def backtrack():
        if len(res) > 0:
            return
        if len(sol) == m * n:
            print(sol)
            if indexesAreNeighbours(sol[0], sol[-1], m, n):
                res.append(sol[:])
            return
        # elif all([i in sol for i in neighbours(sol[0], m, n)]):
        elif len(exploredNB) == len(originNeighbours):
            return
        
        validNeighbours = list(filter(lambda i : i not in sol, neighbours(sol[-1], m, n)))
        # print()
        # print(sol[-1])
        # print(validNeighbours)
        if len(validNeighbours) == 0:
            print(sol)
            return
        for i in validNeighbours:
            if i in originNeighbours:
                exploredNB.append(i)
                sol.append(i)
                backtrack()
                exploredNB.pop()
                sol.pop()
            else:
                sol.append(i)
                backtrack()
                sol.pop()

    # print(sol[0])
    backtrack()
    return res[0]

if __name__=="__main__":
    path = hamiltonianGridPath(5, 5)
    print(path)