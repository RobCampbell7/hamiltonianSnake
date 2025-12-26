# Hamiltonian Snake

## Outline
This project is implemented in Python, it implements an algorithm to play snake in a manner that is guaranteed to eventually win and will never self intersect.

To see this algorithm in action run `./watchSnake.py`

This is done using an algorithm based on an idea I first saw in a [CodeBullet video](https://www.youtube.com/watch?v=tjQIO1rqTBE) which is based on [a project by John Tapsell](https://johnflux.com/tag/snake/).

The idea is to describe a path through the game space such that it visits each square only once and returns to its starting position. This is a Hamiltonian cycle (hopefully this explains the name 'Hamiltonian Snake')

A 'completed' game of snake can be described as full Hamiltonian cycle of the gamespace. A particuarly boring version of this algorithm would simply follow a hamiltonia cycle continually until eventually the snake has eaten every apple and thereby wins. This would be very dull however there is a main optimisation described in John Tapsell's piece that makes this a viable and non-boring method.

At each move we can choose to other follow the cycle or take a shortcut. If this shortcut leads us closer to the apple and maintain's the hamiltonian cycle then we can take it and not risk any collision or self intersection and get a shorter route to the apple.

The implemented method is more complex than this and uses this hamiltonian cycle method as a way of preventing the snake trapping itself or pathfinding through itself and otherwise the program implements A* using Hamiltonian Distance as a heuristic.

### Playing Snake (basically irrelevant)
As an extra that I implemented for some reason you can actual play snake yourself. This can be done by running `./playSnake.py` in this directory and you can play a normal game of snake using the arrow keys for control.

There are a number of visual changes that can be made such as board size and the size of each space which I hope is fairly self explanatory.

## Directory Contents
### README.md
The file you're looking at...

### watchSnake.py
The main file in this project that implements the described method and visualises it using pygame

### hamilSnake.py
Implements the class for the snake with hamiltonian behaviour. This has several useless methods and things I plan to change. But it works at present and effectively implements the snake.

### aStarForSnake.py
This contains the functionality for the pathfinding method of the algorithm using A* and the hamiltonian logic.

### hamilCycles.py
This file contains the functionality for generating hamiltonian cycles, both random and regularly structured. Implements two methods for returning indexes in a grid or coordinates.

### snakePlayer.py and playSnake.py
These files contain the class for running regular snake played by the user and actual file to run and visualise this in pygame.

### aStarTesting/
Files from when I was testing the A* algorithm first to then modify it for our purposes. It is kept for posteristy and in case I accidentally break my implementation and need to refer back.

## TODO
- Change implementation of cycle to instead be a map rather than list to increase lookup speed.
- Potential change in distance heuristic used in A*, something like distance along cycle?
- Alternate method for finding the 'initial moves' in path finding algorithm that make the apple an allowed space. Maybe a double A* implementation who knows?