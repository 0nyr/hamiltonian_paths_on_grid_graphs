import random

# Tikz template
TIKZ_FIG_BEGIN = """
\\begin{figure}
    \\centering
    \\begin{tikzpicture}
        \\tikzstyle{cell} = [draw, thick, minimum size=1cm]

"""

TIKZ_FIG_END = """
    \\end{tikzpicture}
    \\caption{xxx}
    \\label{fig:xxx}
\\end{figure}
"""

class TileGridGraph:
    def __init__(
        self, 
        n: int, 
        m: int, 
    ):
        """
        Creates a default grid graph of size n x m tiles, with no holes.
        """
        self.n = n
        self.m = m

        self.tile_exists = [[True for _ in range(m)] for _ in range(n)]
        
        if self.check_connected_graph() == False:
            raise Exception("The graph is not connected.")
    
    def __get_periphery_indices(self) -> set[tuple[int, int]]:
        """
        Get the periphery indices of the grid.
        A periphery index is an index that is on the periphery of the grid graph.
        This is not only the trivial borders of the grid graph, 
        but also the cells that are adjacent to holes.
        """
        periphery_indices: set[tuple[int, int]] = set()
        for i in range(self.n):
            for j in range(self.m):
                # trivial periphery
                if i in [0, self.n-1] or j in [0, self.m-1]:
                    periphery_indices.add((i, j))
                
                # case where there are already holes on the periphery
                # in such a case, we need to add the cells that are adjacent to the holes
                if self.tile_exists[i][j] == False:
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        # check if the adjacent cell is in the grid
                        if 0 <= i + dx < self.n and 0 <= j + dy < self.m:
                            periphery_indices.add((i + dx, j + dy))
        
        return periphery_indices

    def add_periphery_holes(self, nb_holes: int):
        """
        Add holes that are on the periphery of the grid.
        Ex: (. = hole, x = cell)
        x x . x .
        . x x x .
        . . x x x
        x x x . x
        x . . . .
        """
        def __add_one_periphery_hole():
            # List of all periphery cell indices
            periphery_indices = self.__get_periphery_indices()
            
            # Randomly select 1 tuple 
            return random.sample(sorted(periphery_indices), 1)[0]

        for k in range(nb_holes):
            i, j = __add_one_periphery_hole()
            self.tile_exists[i][j] = False
        
        if self.check_connected_graph() == False:
            raise Exception("The graph is not connected.")

    def check_connected_graph(self) -> bool:
        """
        Check if the graph is connected.
        A connected graph is a graph where there is a path between any two vertices,
        horizontally or vertically.
        There must be no isolated vertices or groups of isolated vertices.

        Ex: (. = hole, x = cell)
        x x . x .
        . x x x .
        . . x x x
        x x x . x
        x . . . .
        This graph is connected.

        Ex: (. = hole, x = cell)
        x x . x .
        . x x x .
        . . x x x
        x x . . x
        x . . . .
        This graph is not connected.
        """
        def dfs(x, y, visited):
            if (x, y) in visited or not (0 <= x < self.n and 0 <= y < self.m) or not self.tile_exists[x][y]:
                return
            visited.add((x, y))
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                dfs(x + dx, y + dy, visited)

        visited = set()
        start_cell: tuple[int, int] | None = None
        # Find the first cell
        for i in range(self.n):
            for j in range(self.m):
                if self.tile_exists[i][j] and start_cell is None:
                    start_cell = (i, j)
                    break

        if start_cell is None:
            return True  # The grid has no cells, thus it's trivially connected.

        dfs(start_cell[0], start_cell[1], visited)

        # Check if all cells are visited
        return all(self.tile_exists[i][j] == ((i, j) in visited) for i in range(self.n) for j in range(self.m))


    def add_holes(self, nb_holes: int):
        """
        Add holes that are not on the periphery of the grid.
        Ex: (. = hole, x = cell)
        x x x x x
        x x x . x
        x . x x x
        x . x x x
        x x x x x
        Those holes are not connected to the periphery.
        """
        # List of all non-periphery cell indices
        periphery_indices = self.__get_periphery_indices()
        inner_indices = [(i, j) for i in range(self.n) for j in range(self.m) if (i, j) not in periphery_indices]

        # Randomly select nb_holes indices to convert to holes, avoiding duplicates
        holes_indices = random.sample(inner_indices, min(nb_holes, len(inner_indices)))

        for i, j in holes_indices:
            self.tile_exists[i][j] = False
    
    def make_narrow(self):
        """
        Expects the grid to be have some holes and periphery holes.
        Remove all cells that are not on the periphery.
        This makes the grid graph narrower.
        """
        # List of all non-periphery cell indices
        periphery_indices = self.__get_periphery_indices()
        inner_indices = [(i, j) for i in range(self.n) for j in range(self.m) if (i, j) not in periphery_indices]

        # Put all inner cells to False
        for i, j in inner_indices:
            self.tile_exists[i][j] = False
        
        if self.check_connected_graph() == False:
            raise Exception("The graph is not connected.")

    def generate_tikz(self, output_path: str):
        """
        Generate the tikz code for the grid graph.

        \\begin{figure}
            \\centering
            \\begin{tikzpicture}
                \\tikzstyle{cell} = [draw, thick, minimum size=1cm]
            
                \node[cell] at (0,0) {};
                \node[cell] at (1,0) {};
                \node[cell] at (1,1) {};
                \node[cell] at (1,2) {};
                \node[cell] at (2,2) {};
            \\end{tikzpicture}
            \\caption{All the different possibilities for the Hamiltonian path to traverse a cell.}
            \\label{fig:xsxs}
        \\end{figure}
        """
        tikz_code = TIKZ_FIG_BEGIN

        tikz_code += "\t\t % Tiles\n"

        # Draw the tiles
        for i in range(self.n):
            for j in range(self.m):
                if self.tile_exists[i][j]:
                    tikz_code += f"\t\t\\draw[fill=gray!20, draw=black, very thick] ({j},{-i}) rectangle ({j+1},{-i-1});\n"
        
        tikz_code += "\n\t\t % Inner cells\n"

        # Draw the inner cells
        for i in range(self.n):
            for j in range(self.m):
                if self.tile_exists[i][j]:
                    tikz_code += f"\t\t\\draw[draw=gray, thin] ({j},{-i}) rectangle ({j+0.5},{-i-0.5});\n"
                    tikz_code += f"\t\t\\draw[draw=gray, thin] ({j},{-i-0.5}) rectangle ({j+0.5},{-i-1});\n"
                    tikz_code += f"\t\t\\draw[draw=gray, thin] ({j+0.5},{-i}) rectangle ({j+1},{-i-0.5});\n"
                    tikz_code += f"\t\t\\draw[draw=gray, thin] ({j+0.5},{-i-0.5}) rectangle ({j+1},{-i-1});\n"

        tikz_code += TIKZ_FIG_END

        with open(output_path, "w") as file:
            file.write(tikz_code)

    def print(self):
        """
        Print the grid graph.
        """
        for i in range(self.n):
            for j in range(self.m):
                print('.' if not self.tile_exists[i][j] else 'x', end=' ')
            print()

def tile_grid_graph_from_text(string: str) -> TileGridGraph:
    """
    Generate a tile grid graph from a string.
    Ex: 
    x x x x x x . 
    x x x . x x x 
    . x x x . . x 
    x . x x . x x 
    x x . x x x x
    """
    # remove tabs
    string = string.replace("\t", "").replace(" ", "")

    lines = string.split("\n")
    n = len(lines)
    m = len(lines[0])
    grid_graph = TileGridGraph(n, m)

    for i in range(n):
        for j in range(m):
            grid_graph.tile_exists[i][j] = lines[i][j] == "x"
    
    return grid_graph





# Tests
import unittest
class TestGridGraph(unittest.TestCase):
    def test_graph_not_connected(self):
        """
        Test to check if the graph is correctly identified as not connected.
        """
        grid_text = """
        x x x x x x .
        x x x . x x x
        . x x x . . x
        x . x x . x x
        x x . x x x x
        """
        grid = tile_grid_graph_from_text(grid_text.strip())
        self.assertFalse(grid.check_connected_graph())

    def test_graph_not_connected_2(self):
        """
        Test to check if the graph is correctly identified as not connected.
        """
        grid_text = """
        x x x x . x x 
        x . x . x x . 
        . x . x x x x 
        x x x x x x x 
        x . x x x x . 
        """
        grid = tile_grid_graph_from_text(grid_text.strip())
        self.assertFalse(grid.check_connected_graph())

    def test_graph_connected(self):
        """
        Test to check if the graph is correctly identified as connected.
        """
        grid_text = """
        . . x x x x x
        x x . x x . x
        . x x x . x .
        x x x x x x x
        x x x . x x x
        """
        grid = tile_grid_graph_from_text(grid_text.strip())
        self.assertTrue(grid.check_connected_graph())
