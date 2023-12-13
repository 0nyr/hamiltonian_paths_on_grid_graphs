from enum import Enum
import random

class RectangleGridCategory(Enum):
    FULL = 0
    PERIPHERY_HOLES = 1
    HOLES = 2

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

class GridGraph:
    def __init__(
        self, 
        n: int, 
        m: int, 
        grid_category: RectangleGridCategory = RectangleGridCategory.FULL,
        nb_holes: int = 0,
    ):
        self.n = n
        self.m = m

        self.cell_exists = [[True for _ in range(m)] for _ in range(n)]

        if grid_category != RectangleGridCategory.FULL and nb_holes == 0:
            self.grid_category = RectangleGridCategory.FULL
        elif grid_category == RectangleGridCategory.FULL:
            self.grid_category = RectangleGridCategory.FULL
        elif grid_category == RectangleGridCategory.PERIPHERY_HOLES:
            self.add_periphery_holes(nb_holes)
            self.grid_category = RectangleGridCategory.PERIPHERY_HOLES
        elif grid_category == RectangleGridCategory.HOLES:
            # Add half of the holes on the periphery and half of the holes inside the grid
            self.add_periphery_holes(nb_holes//2)
            self.add_holes(nb_holes//2)
            self.grid_category = RectangleGridCategory.HOLES
        
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
                if self.cell_exists[i][j] == False:
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
        if self.grid_category == RectangleGridCategory.FULL:
            self.grid_category = RectangleGridCategory.PERIPHERY_HOLES

        def __add_one_periphery_hole():
            # List of all periphery cell indices
            periphery_indices = self.__get_periphery_indices()
            
            # Randomly select 1 tuple 
            return random.sample(sorted(periphery_indices), 1)[0]

        for k in range(nb_holes):
            i, j = __add_one_periphery_hole()
            self.cell_exists[i][j] = False
        
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
            if (x, y) in visited or not (0 <= x < self.n and 0 <= y < self.m) or not self.cell_exists[x][y]:
                return
            visited.add((x, y))
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                dfs(x + dx, y + dy, visited)

        visited = set()
        # Find the first cell
        for i in range(self.n):
            for j in range(self.m):
                if self.cell_exists[i][j]:
                    start_cell = (i, j)
                    dfs(start_cell[0], start_cell[1], visited)
                    break
            if visited:
                break

        # Check if all cells are visited
        return all(self.cell_exists[i][j] == ((i, j) in visited) for i in range(self.n) for j in range(self.m))

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
        if self.grid_category == RectangleGridCategory.FULL:
            self.grid_category = RectangleGridCategory.HOLES

        # List of all non-periphery cell indices
        periphery_indices = self.__get_periphery_indices()
        inner_indices = [(i, j) for i in range(self.n) for j in range(self.m) if (i, j) not in periphery_indices]

        # Randomly select nb_holes indices to convert to holes, avoiding duplicates
        holes_indices = random.sample(inner_indices, min(nb_holes, len(inner_indices)))

        for i, j in holes_indices:
            self.cell_exists[i][j] = False

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
        for i in range(self.n):
            for j in range(self.m):
                if self.cell_exists[i][j]:
                    tikz_code += f"\t\t\\draw[fill=gray!20, draw=black] ({j},{-i}) rectangle ({j+1},{-i-1});\n"
        tikz_code += TIKZ_FIG_END

        with open(output_path, "w") as file:
            file.write(tikz_code)

    def print(self):
        """
        Print the grid graph.
        """
        for i in range(self.n):
            for j in range(self.m):
                print('.' if not self.cell_exists[i][j] else 'x', end=' ')
            print()


if __name__ == "__main__":
    grid = GridGraph(5, 7, RectangleGridCategory.FULL)
    grid.add_periphery_holes(12)
    #grid.add_holes(5)
    grid.print()
    grid.generate_tikz("test.tex")

