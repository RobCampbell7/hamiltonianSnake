# Hamiltonian Snake

## Outline
This project is implemented in Python, it implements an algorithm to play snake in a manner that is intended to eventually win and never self intersect.

To see this algorithm in action run `python3 watchSnake.py`

This is done using an algorithm based on an idea I first saw in a [CodeBullet video](https://www.youtube.com/watch?v=tjQIO1rqTBE) which is based on [a project by John Tapsell](https://johnflux.com/tag/snake/).

The idea is to describe a path through the game space such that it visits each square only once and returns to its starting position. This is a Hamiltonian cycle (hopefully this explains the name 'Hamiltonian Snake')

A 'completed' game of snake can be described as full Hamiltonian cycle of the gamespace. A particularly boring version of this algorithm would simply follow a Hamiltonian cycle continually until eventually the snake has eaten every apple and thereby wins. This would be very dull however there is a main optimisation described in John Tapsell's piece that makes this a viable and non-boring method.

At each move we can choose to either follow the cycle or take a shortcut. If this shortcut leads us closer to the apple and maintains the Hamiltonian cycle then we can take it and not risk any collision or self intersection and get a shorter route to the apple.

The implemented method is more complex than this and uses the Hamiltonian cycle as a way of preventing the snake trapping itself or pathfinding through itself. The current version searches for a route to the apple with a breadth first search over whole snake positions, only allowing moves that keep the body in cycle order. If no such route exists it steps along the cycle instead. An earlier A* version of the search is still in the repository. The pathfinding is in the middle of being reworked, see the TODO list below.

## How it works
The cycle is built in `hamilCycles.py`. A regular cycle is laid out first: along the top row, zigzagging down the rows beneath, then back up the first column. It is then randomised by repeatedly splitting it into two smaller cycles and joining them back together in a different place, which rewires a small patch each time while keeping it a valid Hamiltonian cycle. This needs at least one even side, as a grid with both sides odd has no Hamiltonian cycle.

The snake in `hamilSnake.py` keeps a map from each cell to its position in the cycle. When it has no moves queued it searches for the apple. A move is allowed only if the new head is further round the cycle, measured from the tail, than the old head. Keeping the whole body in cycle order is what stops the snake running into itself.

## Running it
Install pygame and run the visualiser from the repository folder.

```
pip install -r requirements.txt
python3 watchSnake.py
```

Board size, square size and the time between moves are set at the top of `watchSnake.py`. Backspace or closing the window quits. Python 3.10 or later is needed because `snakePlayer.py` uses match statements.

### Playing Snake (basically irrelevant)
As an extra that I implemented for some reason you can actually play snake yourself. This can be done by running `python3 playSnake.py` in this directory and you can play a normal game of snake using the arrow keys for control.

There are a number of visual changes that can be made such as board size and the size of each space which I hope is fairly self explanatory.

## Directory Contents
### `README.md`
The file you're looking at...

### `watchSnake.py`
The main file in this project that implements the described method and visualises it using pygame

### `hamilSnake.py`
Implements the class for the snake with hamiltonian behaviour. This has several useless methods and things I plan to change. But it works at present and effectively implements the snake.

### `breadthFirstForSnake.py`
The pathfinding currently used by `hamilSnake.py`. A breadth first search where each state is the whole snake, restricted to moves that keep the body in cycle order.

### `aStarForSnake.py`
This contains the functionality for the earlier pathfinding method of the algorithm using A* and the hamiltonian logic. It is imported by `hamilSnake.py` but not called at present.

### `hamilCycles.py`
This file contains the functionality for generating hamiltonian cycles, both random and regularly structured. Implements two methods for returning indexes in a grid or coordinates. Running the file on its own prints a cycle before and after ten thousand mutations.

### `snakePlayer.py` and `playSnake.py`
These files contain the class for running regular snake played by the user and actual file to run and visualise this in pygame.

### `aStarTesting/`
Files from when I was testing the A* algorithm first to then modify it for our purposes. It is kept for posterity and in case I accidentally break my implementation and need to refer back.

### `problemValues.txt`
A cycle, snake position and apple that caused trouble during testing. The same values are used in the `__main__` block of `aStarForSnake.py`.

### `requirements.txt`
The only dependency, pygame.

## TODO
- Change implementation of cycle to instead be a map rather than list to increase lookup speed.
- Redo A* method will alternate method of indexing nodes. !important!
