from window import Window, Line, Point


class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1: int | None = None
        self._x2: int | None = None
        self._y1: int | None = None
        self._y2: int | None = None
        self._win: Window | None = win
        self._visited = False

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        wall_positions = [
            (self.has_left_wall, Point(x1, y1), Point(x1, y2)),
            (self.has_top_wall, Point(x1, y1), Point(x2, y1)),
            (self.has_right_wall, Point(x2, y1), Point(x2, y2)),
            (self.has_bottom_wall, Point(x1, y2), Point(x2, y2)),
        ]

        for has_wall, start, end in wall_positions:
            color = "black" if has_wall else "white"
            line = Line(start, end)
            self._win.draw_line(line, color)
        self._win.redraw()

    def set_walls(self, has_left=True, has_top=True, has_right=True, has_bottom=True):
        self.has_left_wall = has_left
        self.has_top_wall = has_top
        self.has_right_wall = has_right
        self.has_bottom_wall = has_bottom

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return

        if self._x1 is None or self._x2 is None or self._y1 is None or self._y2 is None:
            return
        origin_cell_center = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        to_cell_center = Point(
            ((to_cell._x1 + to_cell._x2) / 2), ((to_cell._y1 + to_cell._y2) / 2)
        )

        fill_color = "red" if not undo else "gray"

        # horizontal
        if self._y1 == to_cell._y1:
            start_point = Point(
                min(origin_cell_center._x, to_cell_center._x), origin_cell_center._y
            )
            end_point = Point(
                max(origin_cell_center._x, to_cell_center._x), origin_cell_center._y
            )
        # vertical
        else:
            start_point = Point(
                origin_cell_center._x, min(origin_cell_center._y, to_cell_center._y)
            )
            end_point = Point(
                origin_cell_center._x, max(origin_cell_center._y, to_cell_center._y)
            )

        self._win.draw_line(Line(start_point, end_point), fill_color)
