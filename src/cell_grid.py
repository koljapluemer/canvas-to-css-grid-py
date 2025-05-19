from typing import Literal, get_args, Dict

# each edge cell can have connectors to the four cardinal directions
# we code them with keys like "eNE__", where an existing letter means the connector is present
# and an underscore at the localtion of a cardinal direction means it is not
# cardinal directions are ALWAyS ordered NESW (prefix "e" stands for "edge")
CELL: Dict[str, str] = {
    "edge-N_S_": "|",
    "edge-E_W": "-",
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

    def __init__(self, rows: list[list[str]]):
        self.cells = rows

    def render(self) -> str:
        return "\n".join([" ".join(row) for row in self.cells])
    

    @staticmethod
    def make_one_by_one_grid() -> "CellGrid":
        return CellGrid([["empty"]])
    
    