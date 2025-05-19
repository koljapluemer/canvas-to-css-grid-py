from models.cells import Cell

class Grid:
    rows: list[list[Cell]]
    
    def __init__(self, rows: list[list[Cell]]):
        self.rows = rows

    def render(self) -> str:
        return "\n".join([" ".join([cell.render() for cell in row]) for row in self.rows])
        
        
        
    
    
    