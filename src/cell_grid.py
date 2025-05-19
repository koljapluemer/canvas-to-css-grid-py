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
    "node": "□",
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
        return "\n".join([" ".join(row) for row in self.cells])
    

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
    def clone_column(self, colIndex: int):
        # Get the column to clone
        column_to_clone = [row[colIndex] for row in self.cells]

        # Insert the cloned column to the right of the original
        for i, row in enumerate(self.cells):
            row.insert(colIndex + 1, column_to_clone[i])

    def clone_row(self, rowIndex: int):
        # Get the row to clone
        row_to_clone = self.cells[rowIndex]

        # Insert the cloned row below the original
        self.cells.insert(rowIndex + 1, row_to_clone)

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
        self.cells.insert(index, ["empty"] * len(self.cells[0]))
    
    def add_empty_column_at_index(self, index: int) -> None:
        for row in self.cells:
            row.insert(index, "empty")

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
                if self.cells[i + di][j + dj] == "node":
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
        