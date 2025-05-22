from classes.coordinate import Coordinate
from src.classes.cell import Cell

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell() for _ in range(width)] for _ in range(height)]

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
                grid.cells[row][col].value = value
        
        return grid
    
    def export_to_txt(self):
        # Convert each row of cells to a space-separated string
        lines = []
        for row in self.cells:
            line = ' '.join(cell.value for cell in row)
            lines.append(line)
        
        # Join all lines with newlines
        return '\n'.join(lines)
    

    # everything that fulfills get_is_cell_empty_and_all_neighbors_empty_or_out_of_bounds_at()
    def get_all_valid_node_placement_cells(self) -> list[Cell]:
        return []
    
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
