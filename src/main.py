from hpgg.grid_graphs.cell_grid_graph import CellGridGraph, CellPathMatrix
from hpgg.grid_graphs.tile_grid_graphs import TileGridGraph, tile_grid_graph_from_text

def gen_random_grid_graph(n: int, m: int) -> TileGridGraph:
    """
    Generate a random grid graph of size n x m, with nb_holes holes.
    """
    grid = TileGridGraph(n, m)

    grid.add_periphery_holes(5)
    grid.add_holes(3)
    
    #grid.make_narrow()
    #grid.generate_tikz("test.tex")

    assert grid.check_connected_graph()

    return grid

def gen_from_text_grid_graph() -> TileGridGraph:
    """
    Generate a grid graph from a text.
    """

    grid_text = """
    . x x x x x x
    x x . x x . x
    x x x x . x x
    x . x x x x .
    x x x . x x x
    """
    grid = tile_grid_graph_from_text(grid_text.strip())
    grid.print()
    grid.generate_tikz("test.tex")

    return grid

if __name__ == "__main__":
    # generate grid graph from text
    #gen_from_text_grid_graph()

    # generate random grid graph
    grid = gen_random_grid_graph(5, 7)
    print("Grid graph:")
    grid.print()

    # cell grid graph
    cell_grid_graph = CellGridGraph(grid)
    cell_path_matrix = CellPathMatrix(cell_grid_graph)
    print("Cell grid graph:")
    cell_path_matrix.print()

    
