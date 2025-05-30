import random
from typing import Literal, get_args, Dict
import logging
import os
from datetime import datetime
from grid_logger import GridLogger
from collections import deque

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Set up logging with timestamped filename
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
logging.basicConfig(
    filename=f'logs/grid_operations_{timestamp}.log',
    level=logging.INFO,
    format='%(message)s'
)

class GridNode:
    letter_id: str
    content: str
    col: int
    row: int
    width: int
    height: int

    def __init__(self, content: str, col: int, row: int, width: int, height: int, letter_id: str):
        self.content = content
        self.col = col
        self.row = row
        self.width = width
        self.height = height
        self.letter_id = letter_id

class GridEdge:
    def __init__(self, from_node: GridNode, to_node: GridNode, label: str | None):
        self.from_node = from_node
        self.to_node = to_node
        self.label = label

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
    nodes: list[GridNode]
    edges: list[GridEdge]
    logger: GridLogger
    _next_letter_id: int  # Track next available letter index
    debug_level: int  # 0 = normal, 1 = verbose, 2 = deep debug

    def __init__(self, rows: list[list[str]]):
        self.cells = rows
        self.logger = GridLogger()
        self.nodes = []
        self.edges = []  # Initialize edges attribute
        self._next_letter_id = 0
        self.debug_level = 2  # 0 = normal, 1 = verbose, 2 = deep debug

    def _get_next_letter_id(self) -> str:
        """Get next available letter ID, starting with single letters then moving to pairs."""
        if self._next_letter_id < 26:
            letter = chr(ord('a') + self._next_letter_id)
            self._next_letter_id += 1
            return letter
        else:
            # For IDs beyond 'z', use pairs like 'aa', 'ab', etc.
            first = chr(ord('a') + (self._next_letter_id // 26) - 1)
            second = chr(ord('a') + (self._next_letter_id % 26))
            self._next_letter_id += 1
            return first + second

    def render(self) -> str:
        # render according to the CELL dict
        rendered_cells = []
        for row in self.cells:
            rendered_row = []
            for cell in row:
                rendered_row.append(CELL[cell])
            rendered_cells.append("".join(rendered_row))
        return "\n".join(rendered_cells)
    

    def render_with_named_nodes(self) -> str:
        """Render the grid using node letter_ids."""
        # Start with the basic render
        rendered = self.render().split('\n')
        
        # For each node, overlay its letter_id
        for node in self.nodes:
            for row in range(node.row, node.row + node.height):
                for col in range(node.col, node.col + node.width):
                    if 0 <= row < len(rendered) and 0 <= col < len(rendered[row]):
                        rendered[row] = rendered[row][:col] + node.letter_id + rendered[row][col + 1:]
        
        return '\n'.join(rendered)
    

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
            
        # Update node positions and widths
        for node in self.nodes:
            if node.col > col_index:
                node.col += 1
            elif node.col <= col_index and node.col + node.width > col_index:
                # If the node spans the cloned column, increase its width
                node.width += 1
            
        # Validate again after modification
        row_lengths = [len(row) for row in self.cells]
        if len(set(row_lengths)) != 1:
            raise ValueError(f"Grid has inconsistent row lengths after cloning: {row_lengths}")

    def clone_row(self, row_index: int):
        # Get the row to clone and create a new list
        row_to_clone = self.cells[row_index].copy()
        # Insert the cloned row below the original
        self.cells.insert(row_index + 1, row_to_clone)
        
        # Update node positions and heights
        for node in self.nodes:
            if node.row > row_index:
                node.row += 1
            elif node.row <= row_index and node.row + node.height > row_index:
                # If the node spans the cloned row, increase its height
                node.height += 1

    def clone_random_valid_column_or_row(self) -> None:
        clonable_columns = self.get_clonable_columns()
        clonable_rows = self.get_clonable_rows()
        self.logger.log_step(f"Found {len(clonable_columns)} clonable columns and {len(clonable_rows)} clonable rows", self.render())
        
        will_clone_column = random.random() < 0.5 if clonable_columns and clonable_rows else bool(clonable_columns)
        
        if will_clone_column:
            col_index = random.randrange(len(clonable_columns))
            self.logger.log_step(f"Cloning column at index {col_index}", self.render())
            self.clone_column(col_index)
        else:
            row_index = random.randrange(len(clonable_rows))
            self.logger.log_step(f"Cloning row at index {row_index}", self.render())
            self.clone_row(row_index)
        self.logger.log_step("Grid after cloning", self.render())

    def add_empty_row_at_index(self, index: int) -> None:
        # Validate all rows have the same length
        row_lengths = [len(row) for row in self.cells]
        if len(set(row_lengths)) != 1:
            raise ValueError(f"Grid has inconsistent row lengths: {row_lengths}")
            
        # Create new row with same length as existing rows
        new_row = ["empty"] * len(self.cells[0])
        self.cells.insert(index, new_row)
        
        # Update ALL node positions - any node that starts at or after the insertion point
        # needs its row position updated
        for node in self.nodes:
            if node.row >= index:
                node.row += 1
        
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
            
        # Update ALL node positions - any node that starts at or after the insertion point
        # needs its column position updated
        for node in self.nodes:
            if node.col >= index:
                node.col += 1
            
        # Validate again after modification
        row_lengths = [len(row) for row in self.cells]
        if len(set(row_lengths)) != 1:
            raise ValueError(f"Grid has inconsistent row lengths after adding column: {row_lengths}")

    def add_empty_row_or_column_at_start_or_end_randomly(self) -> None:
        will_add_row = random.random() < 0.5
        will_add_at_start = random.random() < 0.5
        if will_add_row:
            if will_add_at_start:
                self.logger.log_step("Adding empty row at start", self.render())
                self.add_empty_row_at_index(0)
            else:
                self.logger.log_step("Adding empty row at end", self.render())
                self.add_empty_row_at_index(len(self.cells))
        else:
            if will_add_at_start:
                self.logger.log_step("Adding empty column at start", self.render())
                self.add_empty_column_at_index(0)
            else:
                self.logger.log_step("Adding empty column at end", self.render())
                self.add_empty_column_at_index(len(self.cells[0]))
        self.logger.log_step("Grid after adding row/column", self.render())


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
    # define also whether we are N, E, S, W in regards to the node
    def get_valid_anchor_cells_for_node(self, node: GridNode) -> list[tuple[int, int, str]]:
        valid_cells = []
        
        # Check cells above the node
        for col in range(node.col, node.col + node.width):
            if node.row > 0 and self.cells[node.row - 1][col] == "empty":
                valid_cells.append((node.row - 1, col, "N"))
        
        # Check cells below the node
        for col in range(node.col, node.col + node.width):
            if node.row + node.height < len(self.cells) and self.cells[node.row + node.height][col] == "empty":
                valid_cells.append((node.row + node.height, col, "S"))
        
        # Check cells to the left of the node
        for row in range(node.row, node.row + node.height):
            if node.col > 0 and self.cells[row][node.col - 1] == "empty":
                valid_cells.append((row, node.col - 1, "W"))
        
        # Check cells to the right of the node
        for row in range(node.row, node.row + node.height):
            if node.col + node.width < len(self.cells[0]) and self.cells[row][node.col + node.width] == "empty":
                valid_cells.append((row, node.col + node.width, "E"))
        
        return valid_cells
        
    def _can_extend_right(self, row: int, col: int, width: int) -> bool:
        # Check if we can extend two more columns to the right
        if col + width + 1 >= len(self.cells[0]):
            return False
        # Check if both the next column and the one after that are empty
        return (self.cells[row][col + width] == "empty" and 
                self.cells[row][col + width + 1] == "empty")

    def _can_extend_down(self, row: int, col: int, height: int, width: int) -> bool:
        # Check if we can extend two more rows down
        if row + height + 1 >= len(self.cells):
            return False
            
        # Check if all cells in both the next row and the one after that are empty
        return (all(self.cells[row + height][col + i] == "empty" for i in range(width)) and
                all(self.cells[row + height + 1][col + i] == "empty" for i in range(width)))

    def _expand_node(self, row: int, col: int) -> tuple[int, int]:
        self.logger.log_grid_operation(f"Starting node expansion at ({row}, {col})", self)
        # Start with 1x1 node
        width = 1
        height = 1
        
        # Expand right as much as possible
        while self._can_extend_right(row, col, width):
            width += 1
        self.logger.log_grid_operation(f"Expanded right to width {width}", self)
        
        # Expand down as much as possible
        while self._can_extend_down(row, col, height, width):
            height += 1
        self.logger.log_grid_operation(f"Expanded down to height {height}", self)
        
        # Ensure we have enough rows and columns
        while len(self.cells) < row + height:
            self.cells.append(["empty"] * len(self.cells[0]))
        for i in range(len(self.cells)):
            while len(self.cells[i]) < col + width:
                self.cells[i].append("empty")
            
        self.logger.log_grid_operation(f"Final expansion size: {width}x{height}", self)
        return width, height

    def add_node_at_random_empty_cell(self, node_content: str) -> None:
        self.logger.log_grid_operation(f"Starting to add node with content: {node_content}", self)
        
        # 1) Find cells with no node neighbors
        valid_cells = self.get_empty_cells_with_no_node_neighbors()
        self.logger.log_grid_operation(f"Found {len(valid_cells)} valid cells", self)
        
        # 2) If none exist, try to create space
        while not valid_cells:
            self.logger.log_grid_operation("No valid cells found, attempting to create space...", self)
            if random.random() < 0.5:
                self.logger.log_grid_operation("Attempting to add empty row/column...", self)
                self.add_empty_row_or_column_at_start_or_end_randomly()
            else:
                self.logger.log_grid_operation("Attempting to clone row/column...", self)
                self.clone_random_valid_column_or_row()
            valid_cells = self.get_empty_cells_with_no_node_neighbors()
            self.logger.log_grid_operation(f"After space creation, found {len(valid_cells)} valid cells", self)
        
        # 3) Choose random valid cell
        row, col = random.choice(valid_cells)
        # Double check the cell is actually empty
        if self.cells[row][col] != "empty":
            raise ValueError(f"Selected cell at ({row}, {col}) is not empty: {self.cells[row][col]}")
        self.logger.log_grid_operation(f"Selected cell at position ({row}, {col})", self)
        
        # 4) Insert the node and expand it
        width, height = self._expand_node(row, col)
        self.logger.log_grid_operation(f"Expanded node to width={width}, height={height}", self)
        
        # Create and store the node with a letter_id
        node = GridNode(
            content=node_content,
            col=col,
            row=row,
            width=width,
            height=height,
            letter_id=self._get_next_letter_id()
        )
        self.nodes.append(node)
        self.logger.log_grid_operation(f"Created node: {node_content} at ({row}, {col}) with size {width}x{height}", self)
        
        # Fill the grid with the node
        for i in range(row, row + height):
            for j in range(col, col + width):
                self.cells[i][j] = "node"
        
        self.logger.log_grid_operation("Final grid after node placement", self)

    def purge_redundant_columns(self) -> None:
        # First remove entirely empty columns
        for col in range(len(self.cells[0]) - 1, -1, -1):
            if all(row[col] == "empty" for row in self.cells):
                for row in self.cells:
                    row.pop(col)
                for node in self.nodes:
                    if node.col > col:
                        node.col -= 1
                    elif node.col <= col < node.col + node.width:
                        node.width -= 1
                self.logger.log_grid_operation("Removed empty column", self)

        # Then remove redundant columns (only if exactly identical)
        for col in range(len(self.cells[0]) - 1, 0, -1):
            is_identical = True
            mismatch_info = None
            for row in range(len(self.cells)):
                def get_cell_id(r, c):
                    if self.cells[r][c] == "node":
                        for n in self.nodes:
                            if n.col <= c < n.col + n.width and n.row <= r < n.row + n.height:
                                return n.letter_id
                        return "node"  # fallback, should not happen
                    return self.cells[r][c]
                id1 = get_cell_id(row, col)
                id2 = get_cell_id(row, col-1)
                if self.debug_level >= 2:
                    self.logger.log_debug(f"Comparing col {col} vs {col-1} at row {row}: {id1!r} vs {id2!r}")
                if id1 != id2:
                    is_identical = False
                    mismatch_info = (row, col, col-1, id1, id2)
                    break
            if self.debug_level >= 2:
                if is_identical:
                    self.logger.log_debug(f"Column {col} is redundant with column {col-1} (all values identical)")
                else:
                    r, c1, c2, v1, v2 = mismatch_info
                    self.logger.log_debug(f"Column {col} is NOT redundant with column {col-1}: mismatch at row {r}: {v1!r} vs {v2!r}")
            if is_identical:
                for row in self.cells:
                    row.pop(col)
                for node in self.nodes:
                    if node.col > col:
                        node.col -= 1
                    elif node.col <= col < node.col + node.width:
                        node.width -= 1
                self.logger.log_grid_operation("Removed redundant column", self)

    def purge_redundant_rows(self) -> None:
        # First remove entirely empty rows
        for row in range(len(self.cells) - 1, -1, -1):
            if all(cell == "empty" for cell in self.cells[row]):
                self.cells.pop(row)
                for node in self.nodes:
                    if node.row > row:
                        node.row -= 1
                    elif node.row <= row < node.row + node.height:
                        node.height -= 1
                self.logger.log_grid_operation("Removed empty row", self)

        # Then remove redundant rows (only if exactly identical)
        for row in range(len(self.cells) - 1, 0, -1):
            is_identical = True
            mismatch_info = None
            for col in range(len(self.cells[0])):
                def get_cell_id(r, c):
                    if self.cells[r][c] == "node":
                        for n in self.nodes:
                            if n.col <= c < n.col + n.width and n.row <= r < n.row + n.height:
                                return n.letter_id
                        return "node"  # fallback, should not happen
                    return self.cells[r][c]
                id1 = get_cell_id(row, col)
                id2 = get_cell_id(row-1, col)
                if self.debug_level >= 2:
                    self.logger.log_debug(f"Comparing row {row} vs {row-1} at col {col}: {id1!r} vs {id2!r}")
                if id1 != id2:
                    is_identical = False
                    mismatch_info = (col, row, row-1, id1, id2)
                    break
            if self.debug_level >= 2:
                if is_identical:
                    self.logger.log_debug(f"Row {row} is redundant with row {row-1} (all values identical)")
                else:
                    c, r1, r2, v1, v2 = mismatch_info
                    self.logger.log_debug(f"Row {row} is NOT redundant with row {row-1}: mismatch at col {c}: {v1!r} vs {v2!r}")
            if is_identical:
                self.cells.pop(row)
                for node in self.nodes:
                    if node.row > row:
                        node.row -= 1
                    elif node.row <= row < node.row + node.height:
                        node.height -= 1
                self.logger.log_grid_operation("Removed redundant row", self)

    def _update_node_positions_after_purge(self) -> None:
        """Update node positions after purging rows/columns.
        
        This is needed because when we remove rows/columns, the node positions
        become invalid. We need to find where each node's cells are in the new grid.
        """
        if not hasattr(self, 'nodes'):
            return
            
        # For each node, find its new position by looking for its cells
        for node in self.nodes:
            # Find the first occurrence of this node's cells
            found = False
            for i in range(len(self.cells)):
                for j in range(len(self.cells[0])):
                    # Check if this is the start of our node
                    if self.cells[i][j] == "node":
                        # Check if this is the start of our node by looking at width and height
                        is_node_start = True
                        for di in range(node.height):
                            for dj in range(node.width):
                                if (i + di >= len(self.cells) or 
                                    j + dj >= len(self.cells[0]) or 
                                    self.cells[i + di][j + dj] != "node"):
                                    is_node_start = False
                                    break
                            if not is_node_start:
                                break
                        
                        if is_node_start:
                            # Update node position
                            node.row = i
                            node.col = j
                            found = True
                            break
                if found:
                    break

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
                height=max_row - min_row + 1,
                letter_id=letter
            )
            grid.nodes.append(node)
        
        return grid
    

    # grid-based Manhattan pathfinding from one node to another
    # first, get the cell of start and end node down by getting valid anchor cells
    # and choosing a random one from each
    # then, use Manhattan
    # draw the path with the correct symbols by utilizing the CELL dict
    # for example, if a given cell of the edge has a connection above and one to the right, use eNE__

    # cells with node's in them are impassable, as are most edge notes
    # crossing a cell that already contains an edge (= cell name begins with "edge-") has a high cost, but is SOMETIMES allowed
    # the only situations where we may pass an edge is the following:

    # 1) we want to go vertical ("N_S_"), and the cell that we want to use is EXACTLY!! occupied with "_E_W"
    # 2) we want to go horizontal ("_E_W"), and the cell that we want to use is EXACTLY occupied with "N_S_"

    # in these case, we may go to this cell and place in it "edge-NESW": "┼" (the symbol for a horizontal and a vertical edge crossing)
    # no other edge cells may be traversed or reused, ever
    def add_edge(self, from_node: GridNode, to_node: GridNode, label: str | None = None) -> bool:
        self.logger.log_grid_operation(f"Starting to add edge from {from_node.content} to {to_node.content} (label: {label})", self)

        # 1. Get anchor cells
        from_anchors = self.get_valid_anchor_cells_for_node(from_node)
        to_anchors = self.get_valid_anchor_cells_for_node(to_node)
        if not from_anchors or not to_anchors:
            self.logger.log_grid_operation(f"No valid anchor cells for edge from {from_node.content} to {to_node.content}", self)
            return False
        start = random.choice(from_anchors)
        end = random.choice(to_anchors)
        self.logger.log_grid_operation(f"Selected anchors: {start} -> {end}", self)

        rows, cols = len(self.cells), len(self.cells[0])
        queue = deque()
        # Initialize queue with just the coordinates, not the full anchor tuple
        queue.append(((start[0], start[1]), []))
        visited = set()
        visited.add((start[0], start[1]))

        # track the edge cells that end up in the path
        # in the tuple, also track from which direction we came
        # initial direction is calculated from start point to the node itself
        #  is inverse to the direction appended to the anchor tuple
        # E → W, N → S, etc.
        direction_map = {"N": "S", "S": "N", "E": "W", "W": "E"}
        direction_of_node_from_chosen_anchor_point = direction_map[start[2]]
        edge_cell_coordinates = [[start[0], start[1], direction_of_node_from_chosen_anchor_point]]

        def can_traverse(curr, nxt):
            ci, cj = curr
            ni, nj = nxt
            cell = self.cells[ni][nj]
            if cell == "node":
                return False
            if cell.startswith("edge-"):
                # Only allow special crossing cases
                if ci != ni and cell == "edge-E_W":  # vertical move into horizontal edge
                    return True
                if cj != nj and cell == "edge-N_S_":  # horizontal move into vertical edge
                    return True
                return False
            return True

        def get_direction(a, b):
            if a is None or b is None:
                return None
            ai, aj = a
            bi, bj = b
            if ai == bi:
                return "E" if bj > aj else "W"
            elif aj == bj:
                return "S" if bi > ai else "N"
            return None

        # 2. BFS for Manhattan path
        found_path = None
        while queue:
            curr, path = queue.popleft()
            if curr == (end[0], end[1]):
                # When we find the end, add it to our coordinates with direction from previous
                if path:  # if there's a previous cell
                    prev = path[-1]
                    prev_dir = get_direction(prev, curr)
                    edge_cell_coordinates.append([curr[0], curr[1], prev_dir])
                found_path = path + [curr]
                break
            ci, cj = curr
            for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni, nj = ci+di, cj+dj
                if 0 <= ni < rows and 0 <= nj < cols and (ni, nj) not in visited:
                    if can_traverse(curr, (ni, nj)):
                        # Add this cell to our coordinates with direction from current
                        dir_to_next = get_direction(curr, (ni, nj))
                        edge_cell_coordinates.append([ni, nj, dir_to_next])
                        queue.append(((ni, nj), path + [curr]))
                        visited.add((ni, nj))
        if not found_path:
            self.logger.log_grid_operation(f"No path found for edge from {from_node.content} to {to_node.content}", self)
            return False
        self.logger.log_grid_operation(f"Path found for edge: {found_path}", self)

        # 3. Draw the path with correct connectors
        for i, (ci, cj, dir_to_next) in enumerate(edge_cell_coordinates):
            current_cell = self.cells[ci][cj]
            
            # Get the direction we came from (previous cell's dir_to_next)
            dir_from = edge_cell_coordinates[i-1][2] if i > 0 else None
            
            # Get the direction we're going to (current cell's dir_to_next)
            dir_to = dir_to_next

            # Only use actual directions present
            dirs = set()
            if dir_from:
                dirs.add(dir_from)
            if dir_to:
                dirs.add(dir_to)

            # Compose edge key
            key = ["_", "_", "_", "_"]  # N E S W
            for d in dirs:
                if d == "N": key[0] = "N"
                if d == "E": key[1] = "E"
                if d == "S": key[2] = "S"
                if d == "W": key[3] = "W"
            edge_key = "edge-" + "".join(key)
            
            # Special case: crossing
            if current_cell == "edge-E_W" and ("N" in dirs or "S" in dirs):
                edge_key = "edge-NESW"
            if current_cell == "edge-N_S_" and ("E" in dirs or "W" in dirs):
                edge_key = "edge-NESW"
            
            if self.debug_level >= 2:
                self.logger.log_debug(f"Drawing edge at ({ci}, {cj}): {edge_key}, dirs={dirs}, from={dir_from}, to={dir_to}")
            self.cells[ci][cj] = edge_key if edge_key in CELL else "edge-NESW"

        self.logger.log_grid_operation(f"Finished drawing edge from {from_node.content} to {to_node.content}", self)
        self.edges.append(GridEdge(from_node, to_node, label))
        return True