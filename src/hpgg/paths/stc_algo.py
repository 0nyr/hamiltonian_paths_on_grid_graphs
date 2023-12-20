import networkx as nx

from attr import dataclass
from hpgg.grid_graphs.cell_grid_graph import CellGridGraph, CellPath, CellPathMatrix
from hpgg.grid_graphs.tile_grid_graphs import TileGridGraph

class SkeletonSTC():
    """
    A skeleton is a minimum spanning tree of a tile grid graph.
    It contains NodeSTC objects, that are nodes present at the center
    of a tile.
    We can consider a SkeletonSTC as a tile grid graph where each tile
    is a node, connected to adjacent tiles.
    """
    def __init__(
        self,
        tile_grid_graph: TileGridGraph,
    ):
        """
        Construct a skeleton from a tile grid graph.
        """
        self.tile_grid_graph = tile_grid_graph

        # convert tiles to nodes
        self.graph = nx.Graph()
        for i in range(tile_grid_graph.n):
            for j in range(tile_grid_graph.m):
                if tile_grid_graph.tile_exists[i][j]:
                    self.graph.add_node((i, j))
        
        # connect adjacent tiles (nodes)
        for i in range(tile_grid_graph.n):
            for j in range(tile_grid_graph.m):
                if tile_grid_graph.tile_exists[i][j]:
                    # check the 4 adjacent tiles, and connect them if they exist
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        # check if the adjacent cell is in the grid
                        if 0 <= i + dx < tile_grid_graph.n and 0 <= j + dy < tile_grid_graph.m:
                            # check if the adjacent cell exists
                            if tile_grid_graph.tile_exists[i + dx][j + dy]:
                                self.graph.add_edge((i, j), (i + dx, j + dy))
                
        # construct the skeleton from the tile grid graph (using a MST algo like Kruskal)
        self.graph = nx.minimum_spanning_tree(self.graph)

def set_cell_paths_in_vicinity_of_node_stc(
    cell_path_matrix: CellPathMatrix,
    node_stc: tuple[int, int],
    path_codes: list[CellPath],
):
    node_stc_x, node_stc_y = node_stc
    dx_dy_list = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for i in range(4):
        # this cell must exists (since it is in the vicinity of a NodeSTC)
        dx = dx_dy_list[i][0]
        dy = dx_dy_list[i][1]
        cell_x = node_stc_x * 2 + dx
        cell_y = node_stc_y * 2 + dy
        path_code = path_codes[i]
        cell_path_matrix.cell_path_matrix[cell_x][cell_y] = path_code

def AlgorithmSTC(
    cell_grid_graph: CellGridGraph,
) -> CellPathMatrix:
    """
    Algorithm STC
    """

    assert cell_grid_graph.tile_grid_graph.check_connected_graph()

    # Construct the SkeletonSTC, a minimum spanning tree of the grid graph
    skeleton = SkeletonSTC(cell_grid_graph.tile_grid_graph)

    # From the skeleton, construct the CellPathMatrix
    cell_path_matrix = CellPathMatrix(cell_grid_graph)
    for node_stc in skeleton.graph.nodes:
        node_stc_x, node_stc_y = node_stc
        # a single NodeSTC is surrounded by 4 cells
        # we need to determine which correct CellPath to add
        # We need to ensure that the path is coherent with the adjacent cells
        # check:
        # - path continuity
        # - no crossing with EdgeSTC
        # since we are using a STC method, we are guaranteed to find a 
        # valid path for each cells

        # if current node has 4 edges:
        if len(skeleton.graph.edges(node_stc)) == 4:
            """
            ┘└
            ┐┌
            """
            path_codes = [
                CellPath.TOP_RIGHT,
                CellPath.TOP_LEFT,
                CellPath.BOTTOM_LEFT,
                CellPath.BOTTOM_RIGHT,
            ]
            set_cell_paths_in_vicinity_of_node_stc(
                cell_path_matrix, node_stc, path_codes
            )
        elif len(skeleton.graph.edges(node_stc)) == 3:
            """
            4 cases, depending on the orientation of the 3 EdgeSTCs:
            ┘└    │└    ┘│    ──
            ──    │┌    ┐│    ┐┌
            """
            # get the 3 edges of the current NodeSTC
            edges = list(skeleton.graph.edges(node_stc))
            # the missing edge (top, bottom, left or right) gives the orientation
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                # check if the edge is missing
                if (node_stc_x + dx, node_stc_y + dy) not in edges and (node_stc_y + dy, node_stc_x + dx) not in edges:
                    # determine the path codes
                    if dx == 1 and dy == 0:
                        path_codes = [
                            CellPath.TOP_RIGHT,
                            CellPath.TOP_LEFT,
                            CellPath.VERTICAL,
                            CellPath.VERTICAL,
                        ]
                    elif dx == -1 and dy == 0:
                        path_codes = [
                            CellPath.VERTICAL,
                            CellPath.VERTICAL,
                            CellPath.BOTTOM_LEFT,
                            CellPath.BOTTOM_RIGHT,
                        ]
                    elif dx == 0 and dy == 1:
                        path_codes = [
                            CellPath.VERTICAL,
                            CellPath.TOP_LEFT,
                            CellPath.VERTICAL,
                            CellPath.BOTTOM_RIGHT,
                        ]
                    else:
                        path_codes = [
                            CellPath.TOP_RIGHT,
                            CellPath.VERTICAL,
                            CellPath.BOTTOM_LEFT,
                            CellPath.VERTICAL,
                        ]
                    # set the path codes
                    set_cell_paths_in_vicinity_of_node_stc(
                        cell_path_matrix, node_stc, path_codes
                    )
        elif len(skeleton.graph.edges(node_stc)) == 2:
            """
            6 cases, depending on the orientation of the 2 EdgeSTCs:
            ──    ││    ─┐    ┘│    ┌─    │└
            ──    ││    ┐│    ─┘    │┌    └─
            """
            ...
        elif len(skeleton.graph.edges(node_stc)) == 1:
            """
            4 cases, depending on the orientation of the 1 EdgeSTC:
            ┌┐    ┌─    ││    ─┐
            ││    └─    └┘    ─┘
            """
            ...
        else:
            raise Exception("Invalid number of edges for a NodeSTC.")

    # Return the CellPathMatrix
    return cell_path_matrix
