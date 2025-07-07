class Grid:
    def __init__(self, rows, cols, default_color="black"):
        self.rows = rows
        self.cols = cols
        self.grid = [[default_color for _ in range(cols)] for _ in range(rows)]

    def set(self, row, col, color):
        self.grid[row][col] = color

    def get(self, row, col):
        return self.grid[row][col]

    def fill_cell(self, row, col, color):
        """Alias for set() — for semantic clarity."""
        self.set(row, col, color)

    def fill_rect(self, xmin, xmax, ymin, ymax, color):
        """
        Fill a rectangular area with `color`.
        Top-left is (0, 0).
        Args:
            xmin, xmax: horizontal range (columns)
            ymin, ymax: vertical range (rows)
        """
        for r in range(ymin, ymax + 1):
            for c in range(xmin, xmax + 1):
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    self.grid[r][c] = color

    def fill_all(self, color):
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = color

    def as_list(self):
        return self.grid

    def copy(self):
        new_grid = Grid(self.rows, self.cols)
        new_grid.grid = [row.copy() for row in self.grid]
        return new_grid
