"""Simple program using coroutines that simulates Game of Life"""
from collections import namedtuple
from random import choice

ALIVE = '+'
DEAD = '-'
TICK = '#'

Query = namedtuple('Query', ['x', 'y'])
Transition = namedtuple('Transition', ['x', 'y', 'state'])


class Grid(object):
    """Class representing grid of cells"""
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self._grid = []
        for _ in range(self.height):
            self._grid.append([DEAD] * self.width)

    def __str__(self):
        grid = ''
        for row in self._grid:
            grid += '|'.join(row)
            grid += '\n'
        return grid

    def get_state(self, x, y):
        return self._grid[x % self.height][y % self.width]

    def update_state(self, x, y, state):
        self._grid[x % self.height][y % self.width] = state


def count_neighbours(x, y):
    """Coroutine to return number of alive neighbours of cell in position x, y"""
    n = yield Query(x+1, y)
    nw = yield Query(x+1, y+1)
    ne = yield Query(x+1, y-1)
    w = yield Query(x, y+1)
    e = yield Query(x, y-1)
    s = yield Query(x-1, y)
    sw = yield Query(x-1, y+1)
    se = yield Query(x-1, y-1)

    neighbours = [n, nw, ne, w, e, s, sw, se]
    count = sum(neighbour == ALIVE for neighbour in neighbours)
    return count


def game_logic(state, neighbours):
    """"Calculate cell's next state based on current state and number of alive neighbours"""
    if neighbours == 3:
        return ALIVE
    if state == ALIVE and neighbours == 2:
        return ALIVE
    return DEAD


def step_cell(x, y):
    """Coroutine to determine next state of cell in position x, y"""
    state = yield Query(x, y)
    neighbours = yield from count_neighbours(x, y)
    new_state = game_logic(state, neighbours)
    yield Transition(x, y, new_state)


def simulate(height, width):
    """Coroutine to indefinitely generate next states of cells on grid"""
    while True:
        for x in range(height):
            for y in range(width):
                yield from step_cell(x, y)
        yield TICK


def create_random_grid(height, width):
    """Generate starting grid with random cell states"""
    grid = Grid(height, width)
    for x in range(height):
        for y in range(width):
            grid.update_state(x, y, choice((ALIVE, DEAD)))
    return grid


def get_progeny(grid, sim):
    """Get progeny for time n+1 for grid at time n"""
    progeny = Grid(grid.height, grid.width)
    i = next(sim)
    while i is not TICK:
        if isinstance(i, Query):
            i = sim.send(grid.get_state(i.x, i.y))
        else:
            progeny.update_state(i.x, i.y, i.state)
            i = next(sim)
    return progeny


def simulate_n_generations(height, width, generations):
    """Create random grid of height, width and generate progeny for generations"""
    random_grid = create_random_grid(height, width)
    yield random_grid
    sim = simulate(height, width)
    for i in range(1, generations):
        progeny = get_progeny(random_grid, sim)
        yield progeny
        random_grid = progeny


if __name__ == '__main__':
    height = int(input("Grid height"))
    width = int(input("Grid width"))
    generations = int(input("Generations"))
    simul = simulate_n_generations(height, width, generations)
    for i in range(generations):
        print(f'Generation {i}\n')
        print(next(simul))



















