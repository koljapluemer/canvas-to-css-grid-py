import random
from typing import Literal, get_args, Dict



class GridNode:
    content: str
    col: int
    row: int
    width: int
    height: int

    def __init__(self, content: str, col: int, row: int, width: int, height: int):
        self.content = content
        self.col = col
        self.row = row
        self.width = width
        self.height = height

class GridEdge:
    from_node: GridNode
    to_node: GridNode
    label: str | None


# each edge cell can have connectors to the four cardinal directions
# we code them with keys like "eNE__", where an existing letter means the connector is present
# and an underscore at the localtion of a cardinal direction means it is not
# cardinal directions are ALWAyS ordered NESW (prefix "e" stands for "edge")
CELL: Dict[str, str] = {
    "edge-N_S_": "|",
    "edge-E_W": "—",
    "edge-NESW": "┼",
    "edge-_ES_": "┌",
    "edge-__SW": "┐",
    "edge-NE__": "└",
    "edge-N__W": "┘",
    "node": "x",
    "empty": "·"
} 


class CellGrid:
    cells: list[list[str]]

    # these are high-level structures
    # that are NOT directly rendered
    nodes: list[GridNode]
    edges: list[GridEdge]

    def __init__(self, rows: list[list[str]]):
        self.cells = rows

    def render(self) -> str:
        # render according to the CELL dict
        rendered_cells = []
        for row in self.cells:
            rendered_row = []
            for cell in row:
                rendered_row.append(CELL[cell])
            rendered_cells.append("".join(rendered_row))
        return "\n".join(rendered_cells)
    

    @staticmethod
    def make_one_by_one_grid() -> "CellGrid":
        return CellGrid([["empty"]])
    
    def get_rows(self) -> list[list[str]]:
        return self.cells
    
    def get_columns(self) -> list[list[str]]:
        return [list(col) for col in zip(*self.cells)]
    
    def get_clonable_columns(self) -> list[list[str]]:
        # a column is clonable if ALL cells in it are either empty, node,  "edge-N_S_" or "edge-E_W"
        return [col for col in self.get_columns() if all(cell in ["empty", "node", "edge-N_S_", "edge-E_W"] for cell in col)]
    
    def get_clonable_rows(self) -> list[list[str]]:
        # a row is clonable if ALL cells in it are either empty, node,  "edge-N_S_" or "edge-E_W"
        return [row for row in self.get_rows() if all(cell in ["empty", "node", "edge-N_S_", "edge-E_W"] for cell in row)]
    

    # add the same column again to the right of its current position
    def clone_column(self, col_index: int):
        # Validate all rows have the same length
        row_lengths = [len(row) for row in self.cells]
        if len(set(row_lengths)) != 1:
            raise ValueError(f"Grid has inconsistent row lengths: {row_lengths}")
            
        # Get the column to clone
        column_to_clone = [row[col_index] for row in self.cells]

        # Insert the cloned column to the right of the original
        for i, row in enumerate(self.cells):
            row.insert(col_index + 1, column_to_clone[i])
            
        # Validate again after modification
        row_lengths = [len(row) for row in self.cells]
        if len(set(row_lengths)) != 1:
            raise ValueError(f"Grid has inconsistent row lengths after cloning: {row_lengths}")

    def clone_row(self, row_index: int):
        # Get the row to clone and create a new list
        row_to_clone = self.cells[row_index].copy()
        # Insert the cloned row below the original
        self.cells.insert(row_index + 1, row_to_clone)

    def clone_random_valid_column_or_row(self) -> None:
        # Get all clonable columns and rows
        clonable_columns = self.get_clonable_columns()
        clonable_rows = self.get_clonable_rows()
        
        # If there are no clonable columns or rows, return
        if not clonable_columns and not clonable_rows:
            return
        
        # Randomly choose between column and row if both are available
        will_clone_column = random.random() < 0.5 if clonable_columns and clonable_rows else bool(clonable_columns)
        
        if will_clone_column:
            # Get the index of a random clonable column
            col_index = random.randrange(len(clonable_columns))
            self.clone_column(col_index)
        else:
            # Get the index of a random clonable row
            row_index = random.randrange(len(clonable_rows))
            self.clone_row(row_index)

    def add_empty_row_at_index(self, index: int) -> None:
        # Validate all rows have the same length
        row_lengths = [len(row) for row in self.cells]
        if len(set(row_lengths)) != 1:
            raise ValueError(f"Grid has inconsistent row lengths: {row_lengths}")
            
        # Create new row with same length as existing rows
        new_row = ["empty"] * len(self.cells[0])
        self.cells.insert(index, new_row)
        
        # Validate again after modification
        row_lengths = [len(row) for row in self.cells]
        if len(set(row_lengths)) != 1:
            raise ValueError(f"Grid has inconsistent row lengths after adding row: {row_lengths}")

    def add_empty_column_at_index(self, index: int) -> None:
        # Validate all rows have the same length
        row_lengths = [len(row) for row in self.cells]
        if len(set(row_lengths)) != 1:
            raise ValueError(f"Grid has inconsistent row lengths: {row_lengths}")
            
        for row in self.cells:
            row.insert(index, "empty")
            
        # Validate again after modification
        row_lengths = [len(row) for row in self.cells]
        if len(set(row_lengths)) != 1:
            raise ValueError(f"Grid has inconsistent row lengths after adding column: {row_lengths}")

    def add_empty_row_or_column_at_start_or_end_randomly(self) -> None:
        will_add_row = random.random() < 0.5
        will_add_at_start = random.random() < 0.5
        if will_add_row:
            if will_add_at_start:
                self.add_empty_row_at_index(0)
            else:
                self.add_empty_row_at_index(len(self.cells))
        else:
            if will_add_at_start:
                self.add_empty_column_at_index(0)
            else:
                self.add_empty_column_at_index(len(self.cells[0]))


    def get_empty_cells(self) -> list[tuple[int, int]]:
        return [(i, j) for i, row in enumerate(self.cells) for j, cell in enumerate(row) if cell == "empty"]
    

    def cell_has_at_least_one_node_neighbor(self, i: int, j: int) -> bool:
        # diagonal neighbors count as neighbors
        # we need to check all 8 possible neighbors
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                # Check if the neighbor coordinates are within bounds
                ni, nj = i + di, j + dj
                if (0 <= ni < len(self.cells) and 
                    0 <= nj < len(self.cells[0]) and 
                    self.cells[ni][nj] == "node"):
                    return True
        return False
    
    def get_empty_cells_with_no_node_neighbors(self) -> list[tuple[int, int]]:
        return [
            (i, j) 
            for i, row in enumerate(self.cells) 
            for j, cell in enumerate(row) 
            if cell == "empty" and not self.cell_has_at_least_one_node_neighbor(i, j)
        ]
    
    def get_node_cells(self) -> list[tuple[int, int]]:
        return [(i, j) for i, row in enumerate(self.cells) for j, cell in enumerate(row) if cell == "node"]


    # get all cells around a node that are empty
    # diagonals are NOT valid
    # nodes can span several cells as a rectangle
    # therefore, we need to consider the node's width and height
    def get_valid_anchor_cells_for_node(self, node: GridNode) -> list[tuple[int, int]]:
        valid_cells = []
        
        # Check cells above the node
        for col in range(node.col, node.col + node.width):
            if node.row > 0 and self.cells[node.row - 1][col] == "empty":
                valid_cells.append((node.row - 1, col))
        
        # Check cells below the node
        for col in range(node.col, node.col + node.width):
            if node.row + node.height < len(self.cells) and self.cells[node.row + node.height][col] == "empty":
                valid_cells.append((node.row + node.height, col))
        
        # Check cells to the left of the node
        for row in range(node.row, node.row + node.height):
            if node.col > 0 and self.cells[row][node.col - 1] == "empty":
                valid_cells.append((row, node.col - 1))
        
        # Check cells to the right of the node
        for row in range(node.row, node.row + node.height):
            if node.col + node.width < len(self.cells[0]) and self.cells[row][node.col + node.width] == "empty":
                valid_cells.append((row, node.col + node.width))
        
        return valid_cells
        
    def _can_extend_right(self, row: int, col: int, width: int) -> bool:
        # Check if we can extend one more column to the right
        if col + width >= len(self.cells[0]):
            return False
        return self.cells[row][col + width] == "empty"

    def _can_extend_down(self, row: int, col: int, height: int, width: int) -> bool:
        # Check if we can extend one more row down
        if row + height >= len(self.cells):
            return False
            
        # Check if all cells in the next row are empty
        return all(
            self.cells[row + height][col + i] == "empty" 
            for i in range(width)
        )

    def _expand_node(self, row: int, col: int) -> tuple[int, int]:
        # Start with 1x1 node
        width = 1
        height = 1
        
        # Expand right as much as possible
        while self._can_extend_right(row, col, width):
            width += 1
            
        # Ensure all rows have enough cells for the width
        for i in range(len(self.cells)):
            while len(self.cells[i]) < col + width:
                self.cells[i].append("empty")
            
        # Expand down as much as possible
        while self._can_extend_down(row, col, height, width):
            height += 1
            
        # Ensure we have enough rows
        while len(self.cells) < row + height:
            self.cells.append(["empty"] * len(self.cells[0]))
            
        return width, height

    def add_node_at_random_empty_cell(self, node_content: str) -> None:
        # 1) Find cells with no node neighbors
        valid_cells = self.get_empty_cells_with_no_node_neighbors()
        
        # 2) If none exist, try to create space
        while not valid_cells:
            # 50% chance for each operation
            if random.random() < 0.5:
                self.add_empty_row_or_column_at_start_or_end_randomly()
            else:
                self.clone_random_valid_column_or_row()
            valid_cells = self.get_empty_cells_with_no_node_neighbors()
        
        # 4) Choose random valid cell
        row, col = random.choice(valid_cells)
        
        # 5) Insert the node and expand it
        width, height = self._expand_node(row, col)
        
        # Create and store the node
        node = GridNode(node_content, col, row, width, height)
        if not hasattr(self, 'nodes'):
            self.nodes = []
        self.nodes.append(node)
        
        # Fill the grid with the node
        for i in range(row, row + height):
            for j in range(col, col + width):
                self.cells[i][j] = "node"


    def purge_redundant_columns(self) -> None:
        # a column is redundant if the column to its left has EXACTLY the same content (if it exists)
        # if it redundant in this way, remove it from the grid
        # reverse traversal so we don't mess up the index
        for col in range(len(self.cells[0]) - 1, 0, -1):  # start from rightmost column, go left
            # Get the current column and the one to its left
            current_col = [row[col] for row in self.cells]
            left_col = [row[col - 1] for row in self.cells]
            
            # If they're identical, remove the current column
            if current_col == left_col:
                for row in self.cells:
                    row.pop(col)

    def purge_redundant_rows(self) -> None:
        # a row is redundant if the row above it has EXACTLY the same content (if it exists)
        # if it redundant in this way, remove it from the grid
        # reverse traversal so we don't mess up the index
        for row in range(len(self.cells) - 1, 0, -1):  # start from bottom row, go up
            # If current row is identical to the one above it, remove it
            if self.cells[row] == self.cells[row - 1]:
                self.cells.pop(row)

    @staticmethod
    def from_string(grid_str: str) -> "CellGrid":
        """Create a grid from a string representation.
        
        Example:
            grid_str = '''
            aa→b·
            ····c
            '''
            - Same letters represent the same node
            - '·' represents empty cells
            - '→' represents edge cells
            
        Raises:
            ValueError: If a letter is used for multiple disconnected nodes
            ValueError: If a node is not a solid rectangle
        """
        # Split into lines and remove empty lines
        lines = [line.strip() for line in grid_str.strip().split('\n') if line.strip()]
        
        # Create the grid with empty cells
        height = len(lines)
        width = len(lines[0])
        grid = CellGrid([["empty" for _ in range(width)] for _ in range(height)])
        
        # Track nodes by their letter
        nodes_by_letter: dict[str, list[tuple[int, int]]] = {}
        
        # First pass: collect all cells for each node
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == '·':
                    continue
                elif char == '→':
                    grid.cells[i][j] = "edge-E_W"
                else:
                    # This is a node cell
                    grid.cells[i][j] = "node"
                    if char not in nodes_by_letter:
                        nodes_by_letter[char] = []
                    nodes_by_letter[char].append((i, j))
        
        # Validate each node is a solid rectangle
        for letter, cells in nodes_by_letter.items():
            # Find the bounding box of the node
            min_row = min(i for i, _ in cells)
            max_row = max(i for i, _ in cells)
            min_col = min(j for _, j in cells)
            max_col = max(j for _, j in cells)
            
            # Check if all cells in the bounding box are part of this node
            for i in range(min_row, max_row + 1):
                for j in range(min_col, max_col + 1):
                    if (i, j) not in cells:
                        raise ValueError(f"Node '{letter}' is not a solid rectangle")
        
        # Second pass: create GridNode objects for each letter
        grid.nodes = []
        for letter, cells in nodes_by_letter.items():
            # Find the bounding box of the node
            min_row = min(i for i, _ in cells)
            max_row = max(i for i, _ in cells)
            min_col = min(j for _, j in cells)
            max_col = max(j for _, j in cells)
            
            # Create the node
            node = GridNode(
                content=letter,
                col=min_col,
                row=min_row,
                width=max_col - min_col + 1,
                height=max_row - min_row + 1
            )
            grid.nodes.append(node)
        
        return grid