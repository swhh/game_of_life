from turtle import Turtle, Screen
import gol
import time
from itertools import chain
import sys

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600
BG_COLOR = 'black'
SHAPE_SIZE = 21

screen = Screen()
screen.bgcolor(BG_COLOR)
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.title('Game of Life')
screen.tracer(0)


class Cell(Turtle):
    def __init__(self, position, living=gol.DEAD):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.pu()
        self.goto(position)
        self.state = living
        if self.state is gol.DEAD:
            self.hideturtle()

    def update_cell(self, state):
        if self.state is state:
            return
        if state is gol.DEAD:
            self.hideturtle()
            self.state = gol.DEAD
        else:
            self.showturtle()
            self.state = gol.ALIVE


class CellManager:

    def __init__(self, grid):
        self._cells = []
        for x in range(grid.height):
            self._cells.append([])
            for y in range(grid.width):
                cell = Cell(position=(y*SHAPE_SIZE - SCREEN_WIDTH / 2, x*-SHAPE_SIZE + SCREEN_HEIGHT / 2),
                            living=grid.get_state(x, y))
                self._cells[x].append(cell)

    def update_cells(self, progeny):
        for x in range(progeny.height):
            for y in range(progeny.width):
                cell = self._cells[x][y]
                cell.update_cell(progeny.get_state(x, y))
                assert cell.state == progeny.get_state(x, y)

    def live_cell_count(self):
        return sum(cell.state == gol.ALIVE for cell in chain.from_iterable(self._cells))


if __name__ == '__main__':
    generations, height, width = map(int, sys.argv[1:4])
    speed = float(sys.argv[4])
    simulation = gol.simulate_n_generations(height, width, generations)
    progeny = next(simulation)
    cell_manager = CellManager(progeny)
    for i in range(1, generations):
        time.sleep(speed)
        screen.update()
        progeny = next(simulation)
        cell_manager.update_cells(progeny)














