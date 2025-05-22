from src.classes.cell import Cell
class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell() for _ in range(width)] for _ in range(height)]

    @staticmethod
    def create_from_txt(txt_data):
        return 