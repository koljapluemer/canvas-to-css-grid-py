from classes.coordinate import Coordinate
from src.classes.cell import Cell, CellType
import random

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell(row, col, CellType.EMPTY, None, None, False, False, value="·") for col in range(width)] for row in range(height)]

    @staticmethod
    def create_from_txt(txt_data):
        # Split the text into lines and remove any empty lines
        lines = [line.strip() for line in txt_data.split('\n') if line.strip()]
        
        # Calculate dimensions
        height = len(lines)
        width = len(lines[0].split())  # Split on whitespace to get width
        
        # Create a new grid with these dimensions
        grid = Grid(width, height)
        
        # Set cell values from the text
        for row, line in enumerate(lines):
            values = line.split()
            for col, value in enumerate(values):
                if value == "·":
                    grid.cells[row][col] = Cell(row, col, CellType.EMPTY, None, None, False, False, value="·", occupant_id=None)
                elif value.isalpha():
                    grid.cells[row][col] = Cell(row, col, CellType.NODE, None, None, False, False, value="·", occupant_id=value)
                else:
                    grid.cells[row][col] = Cell(row, col, CellType.EDGE, None, None, False, False, value="·", occupant_id=value)
        
        return grid
    
    def export_to_txt(self):
        # Convert each row of cells to a space-separated string, with trailing space
        lines = []
        for row in self.cells:
            line = ' '.join(cell.render_txt() for cell in row) + ' '  # Add trailing space
            lines.append(line.rstrip())  # Remove trailing space from last line
        return '\n'.join(lines)
    
    def render_to_flow_txt(self):
        # Render each cell using its render_flow method
        lines = []
        for row in self.cells:
            line = ' '.join(cell.render_flow() for cell in row)
            lines.append(line)
        return '\n'.join(lines)

    # everything that fulfills get_is_cell_empty_and_all_neighbors_empty_or_out_of_bounds_at()
    def get_all_valid_node_placement_cells(self) -> list[Cell]:
        valid_cells = []
        for row in range(self.height):
            for col in range(self.width):
                if not self.is_cell_empty(row, col):
                    continue
                # Check all 8 neighbors
                all_neighbors_empty_or_oob = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc
                        if not self.is_cell_empty_or_out_of_bounds(nr, nc):
                            all_neighbors_empty_or_oob = False
                            break
                    if not all_neighbors_empty_or_oob:
                        break
                if all_neighbors_empty_or_oob:
                    valid_cells.append(self.cells[row][col])
        return valid_cells
    
    def is_cell_empty(self, row: int, col: int) -> bool:
        if not (0 <= row < self.height and 0 <= col < self.width):
            return False
        return self.cells[row][col].is_empty()
    
    def is_cell_empty_or_out_of_bounds(self, row: int, col: int) -> bool:
        if not (0 <= row < self.height and 0 <= col < self.width):
            return True
        return self.cells[row][col].is_empty()
    
    def get_all_empty_cells(self) -> list[tuple[int, int]]:
        empty_cells = []
        for row in range(self.height):
            for col in range(self.width):
                if self.cells[row][col].is_empty():
                    empty_cells.append((row, col))
        return empty_cells

    def get_random_valid_node_placement_cell(self) -> tuple[int, int] | None:
        valid_cells = self.get_all_valid_node_placement_cells()
        if not valid_cells:
            return None
        cell = random.choice(valid_cells)
        return (cell.row, cell.col)

    def add_row_to_end(self):
        # Create new row of empty cells
        new_row = [Cell(self.height, col, CellType.EMPTY, None, None, False, False, value="·") for col in range(self.width)]
        self.cells.append(new_row)
        self.height += 1

    def add_col_to_end(self):
        # Add a new empty cell to each row
        for row in range(self.height):
            self.cells[row].append(Cell(row, self.width, CellType.EMPTY, None, None, False, False, value="·"))
        self.width += 1

    def find_manhattan_path(self, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
        """Find a Manhattan path between two points using only empty cells.
        
        Args:
            start: (row, col) of start point
            end: (row, col) of end point
            
        Returns:
            List of (row, col) coordinates forming the path, including start and end points.
            Returns empty list if no path exists.
        """
        if not self.is_cell_empty_or_out_of_bounds(start[0], start[1]) or not self.is_cell_empty_or_out_of_bounds(end[0], end[1]):
            return []
            
        path = [start]
        current = start
        
        # First move horizontally
        while current[1] != end[1]:
            next_col = current[1] + (1 if end[1] > current[1] else -1)
            if not self.is_cell_empty_or_out_of_bounds(current[0], next_col):
                return []  # No path exists
            current = (current[0], next_col)
            path.append(current)
            
        # Then move vertically
        while current[0] != end[0]:
            next_row = current[0] + (1 if end[0] > current[0] else -1)
            if not self.is_cell_empty_or_out_of_bounds(next_row, current[1]):
                return []  # No path exists
            current = (next_row, current[1])
            path.append(current)
            
        return path

    def find_manhattan_path_with_forced_ends(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        start_dir: str,  # 'N', 'S', 'E', 'W'
        end_dir: str     # 'N', 'S', 'E', 'W'
    ) -> list[tuple[int, int]]:
        """
        Find a Manhattan path from start to end, where:
        - The first move from start is in start_dir (direction of breathing space)
        - The last move into end is from end_dir (direction of breathing space)
        Returns the path including start and end, or [] if not possible.
        """
        # Direction deltas
        DIRS = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
        
        # First move from start must be in start_dir (breathing space direction)
        dr, dc = DIRS[start_dir]
        first = (start[0] + dr, start[1] + dc)
        if not (0 <= first[0] < self.height and 0 <= first[1] < self.width and self.is_cell_empty(first[0], first[1])):
            return []
            
        # Last move into end must be from end_dir (breathing space direction)
        dr_end, dc_end = DIRS[end_dir]
        pre_end = (end[0] + dr_end, end[1] + dc_end)
        if not (0 <= pre_end[0] < self.height and 0 <= pre_end[1] < self.width and self.is_cell_empty(pre_end[0], pre_end[1])):
            return []
            
        # BFS from first to pre_end
        from collections import deque
        queue = deque()
        queue.append((first, [start, first]))
        visited = set()
        visited.add(first)
        
        while queue:
            (r, c), path = queue.popleft()
            if (r, c) == pre_end:
                return path + [end]
                
            # Try directions in order: E, S, W, N (prefer right and down)
            for dir_name in ['E', 'S', 'W', 'N']:
                dr, dc = DIRS[dir_name]
                nr, nc = r + dr, c + dc
                if (0 <= nr < self.height and 0 <= nc < self.width and
                    self.is_cell_empty(nr, nc) and (nr, nc) not in visited):
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))
                    
        return []