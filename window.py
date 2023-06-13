from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width=480, height=360):
        self._root = Tk()
        self._root.title("Maze Solver")
        self._root.protocol("WM_DELETE_WINDOW", self.close)
        self._canvas = Canvas(self._root, bg="lightgreen", height=height, width=width)
        self._canvas.pack(fill=BOTH, expand=1)
        self._is_running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self._canvas, fill_color)

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self._is_running = True
        while self._is_running:
            self.redraw()

    def close(self):
        self._is_running = False


class Point:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y


class Line:
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self._p1._x, self._p1._y, self._p2._x, self._p2._y, fill=fill_color, width=2
        )
        canvas.pack(fill=BOTH, expand=1)
