from cell import Cell
import time
import random


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for _ in range(self._num_cols):
            cols = []
            for _ in range(self._num_rows):
                cols.append(Cell(self._win))
            self._cells.append(cols)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.002)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        # mark current cell as visited
        self._cells[i][j]._visited = True

        while True:
            next_indexes = []
            next_poss_index = 0

            # left
            if i > 0 and not self._cells[i - 1][j]._visited:
                next_indexes.append((i - 1, j))
                next_poss_index += 1
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j]._visited:
                next_indexes.append((i + 1, j))
                next_poss_index += 1
            # up
            if j > 0 and not self._cells[i][j - 1]._visited:
                next_indexes.append((i, j - 1))
                next_poss_index += 1
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1]._visited:
                next_indexes.append((i, j + 1))
                next_poss_index += 1

            # nowhere to go from (i, j)
            if next_poss_index == 0:
                self._draw_cell(i, j)
                return

            direction = random.randrange(next_poss_index)
            next_index = next_indexes[direction]

            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False

            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell._visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()

        self._cells[i][j]._visited = True

        # we escaped!
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # move left
        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j]._visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        # move right
        if (
            i < self._num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j]._visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # move down
        if (
            j < self._num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1]._visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        # move up
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1]._visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)
