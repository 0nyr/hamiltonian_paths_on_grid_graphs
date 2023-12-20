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

class CellPath():
    """
    A cell path is a path that is defined on a cell of a cell grid graph.
    6 possible paths are possible through a cell.
    """