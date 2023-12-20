

from attr import dataclass
from hpgg.grid_graphs.cell_grid_graph import CellGridGraph, CellPathMatrix

class SkeletonSTC():
    """
    A skeleton is a minimum spanning tree of a tile grid graph.
    """
    pass

def AlgorithmSTC(
    cell_grid_graph: CellGridGraph,
) -> CellPathMatrix:
    """
    Algorithm STC
    """

    assert cell_grid_graph.tile_grid_graph.check_connected_graph()

    # Construct the SkeletonSTC, a minimum spanning tree of the grid graph
    
    # From the skeleton, construct the CellPathMatrix
    cell_path_matrix = CellPathMatrix(cell_grid_graph)

    # Return the CellPathMatrix
    return cell_path_matrix
