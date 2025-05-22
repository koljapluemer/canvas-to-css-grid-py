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
    