from enum import Enum

class CellPath(Enum):
    """
    A cell path is a path that is defined on a cell of a cell grid graph.
    6 possible paths are possible through a cell.

    If a cell doesn't exist, then it is represented as:

    NO_CELL: ' '
    ┌······┐
    ········
    ········
    └······┘


    A normal cell without path is represented as:

    NO_PATH: 'x'
    ┌──────┐
    │      │
    │      │
    └──────┘

    A cell can have 6 different paths going through it:

    HORIZONTAL (a): '─'
    ┌───┬──┐
    │   |  │
    │   |  │
    └───┴──┘

    VERTICAL (b): '│'
    ┌──────┐
    │______│
    │      │
    └──────┘
    
    BOTTOM_LEFT (c): '┐'
    ┌──────┐
    │---┐  │
    │   |  │
    └───┴──┘
        
    TOP_RIGHT (d):  '┘'
    ┌───┬──┐
    │   |  │
    │---┘  │
    └──────┘

    TOP_LEFT (e): '└'
    ┌───┬──┐
    │   |  │
    │   └--│
    └──────┘

    BOTTOM_RIGHT (f): '┌'
    ┌──────┐
    │   ┌--│
    │   |  │
    └───┴──┘
    """
    NO_CELL = -1
    NO_PATH = 0
    HORIZONTAL = 1
    VERTICAL = 2
    BOTTOM_LEFT = 3
    TOP_RIGHT = 4
    TOP_LEFT = 5
    BOTTOM_RIGHT = 6

CELL_PATH_TO_CHAR = {
    CellPath.NO_CELL: ' ',
    CellPath.NO_PATH: 'x',
    CellPath.HORIZONTAL: '─',
    CellPath.VERTICAL: '│',
    CellPath.BOTTOM_LEFT: '┐',
    CellPath.TOP_RIGHT: '┘',
    CellPath.TOP_LEFT: '└',
    CellPath.BOTTOM_RIGHT: '┌',
}


class CellGridGraph():
    """
    A cell grid graph is a G4 graph where the cells are the vertices.
    Such a grid graph can be defined from a given tile grid graph.
    Each tile contains a group of 2x2 adjacent cells. 
    """
    def __init__(self, tile_grid_graph):
        self.tile_grid_graph = tile_grid_graph

    def cell_exists(self, x, y):
        x_tile = x // 2
        y_tile = y // 2

        # check that the coordinates are in the grid
        if not (
            0 <= x_tile < self.tile_grid_graph.n and 
            0 <= y_tile < self.tile_grid_graph.m
        ):
            return False

        return self.tile_grid_graph.tile_exists[x_tile][y_tile]

    def get_nb_rows(self) -> int:
        return self.tile_grid_graph.n * 2
    
    def get_nb_columns(self) -> int:
        return self.tile_grid_graph.m * 2

class CellPathMatrix():
    def __init__(self, cell_grid_graph: CellGridGraph):
        self.rows = cell_grid_graph.get_nb_rows()
        self.cols = cell_grid_graph.get_nb_columns()

        # initialize the matrix with no path on each cell
        cell_path_matrix = []
        for i in range(self.rows*2):
            cell_path_matrix.append([])
            for j in range(self.cols*2):
                if cell_grid_graph.cell_exists(i, j):
                    cell_path_matrix[i].append(CellPath.NO_PATH)
                else:
                    cell_path_matrix[i].append(CellPath.NO_CELL)
        self.cell_path_matrix = cell_path_matrix

    def print(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(CELL_PATH_TO_CHAR[self.cell_path_matrix[i][j]], end='') 
            print()