from window import Window
from maze import Maze
import sys


def main():
    win_x = 480
    win_y = 360
    margin = 16
    cols = 24
    rows = 18
    cell_size_x = (win_x - 2 * margin) / cols
    cell_size_y = (win_y - 2 * margin) / rows

    sys.setrecursionlimit(10000)
    win = Window(win_x, win_y)

    maze = Maze(margin, margin, rows, cols, cell_size_x, cell_size_y, win, 10)
    is_solvable = maze.solve()
    if not is_solvable:
        print("maze cannot be solved!")
    else:
        print("maze solved!")
    win.wait_for_close()


main()
