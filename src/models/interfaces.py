from typing import Protocol, List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.cells import Cell

class CellContainer(Protocol):
    """Interface for anything that contains cells"""
    cells: List['Cell']

class Renderable(Protocol):
    """Interface for anything that can be rendered to a string"""
    def render(self) -> str: ...

class Connectable(Protocol):
    """Interface for anything that can be connected to other components"""
    def get_connections(self) -> List['Connectable']: ... 