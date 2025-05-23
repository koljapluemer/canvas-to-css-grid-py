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
        # Convert each row of cells to a space-separated string
        lines = []
        for row in self.cells:
            line = ' '.join(cell.render_txt() for cell in row)
            lines.append(line)
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
        return self.cells[row][col].value == "·"
    
    def is_cell_empty_or_out_of_bounds(self, row: int, col: int) -> bool:
        if not (0 <= row < self.height and 0 <= col < self.width):
            return True
        return self.cells[row][col].value == "·"
    
    def get_all_empty_cells(self) -> list[tuple[int, int]]:
        empty_cells = []
        for row in range(self.height):
            for col in range(self.width):
                if self.cells[row][col].value == "·":
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