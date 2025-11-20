from functools import cache
from random import choice, randint, sample, shuffle

def indexToCoord(index, m, n):
    # for an m x n grid
    return (index % m, index // m)

def coordToIndex(x, y, m, n):
    return y * m + x

def randNeighbours(index, m, n):
    nbs = neighbours(index, m, n)
    # if -1 in nbs:
    #     print(index, m, n)
    shuffle(nbs)
    return nbs

@cache
def neighbours(index, m, n):
    x, y = indexToCoord(index, m, n)
    nbours = []
    if x < m - 1:
        # print("b")
        # print(index + 1)
        nbours.append(index + 1)
    if y < n - 1:
        # print("d")
        # print(index + m)
        nbours.append(index + m)
    if x > 0:
        # print("a")
        # print(index - 1)
        nbours.append(index - 1)
    if y > 0:
        # print("c")
        # print(index - m)
        nbours.append(index - m)
    
    return nbours
    # return list(filter(lambda i : indexInBounds(i, m, n), nbours))

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
    # res, sol, exploredNB = [], [coordToIndex(m//2, n//2, m, n)], []
    # res, sol, exploredNB = [], [(m * n) // 2], []
    res, sol, exploredNB = [], [0], []
    originNeighbours = neighbours(sol[0], m, n)
    def backtrack():
        if len(res) > 0: #or sol[-1] in sol[:-1]:
            # print(sol)
            return
        if len(sol) == m * n:
            # print(sol)
            # if indexesAreNeighbours(sol[0], sol[-1], m, n):
            res.append(sol[:])
            return
        # elif all([i in sol for i in neighbours(sol[0], m, n)]):
            # print(sol)
        elif len(exploredNB) == len(originNeighbours):
            # print(sol)
            return
        
        # print()
        # print(sol[-1])
        # print(validNeighbours)
        # if len(validNeighbours) == 0:
        #     # print(sol)
        #     return
        for i in randNeighbours(sol[-1], m, n):
            if i in sol:
                continue
            elif i in originNeighbours:
            # if i in originNeighbours:
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
    path = hamiltonianGridPath(30, 30)
    print(path)
    # print( indexToCoord(2, 3, 2))
    # print(neighbours(2, 3, 2))