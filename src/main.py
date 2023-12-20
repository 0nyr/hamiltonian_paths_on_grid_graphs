from hpgg.grid_graphs.tile_grid_graphs import TileGridGraph, tile_grid_graph_from_text

def gen_random_grid_graph(n: int, m: int) -> TileGridGraph:
    """
    Generate a random grid graph of size n x m, with nb_holes holes.
    """
    grid = TileGridGraph(n, m)

    grid.add_periphery_holes(5)
    grid.add_holes(3)
    #grid.make_narrow()
    grid.print()
    grid.generate_tikz("test.tex")

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
    # generate random grid graph
    #grid = gen_random_grid_graph(5, 5)

    # generate grid graph from text
    gen_from_text_grid_graph()
