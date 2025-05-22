import logging
import os
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cell_grid import CellGrid

class GridLogger:
    def __init__(self):
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Set up logging with timestamped filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        logging.basicConfig(
            filename=f'logs/grid_operations_{timestamp}.log',
            level=logging.INFO,
            format='%(message)s'
        )
        self.steps = []
    
    def log_step(self, message: str, grid: str) -> None:
        """Log a step in the grid manipulation process."""
        self.steps.append({
            'message': message,
            'grid': grid
        })
        logging.info(f"\n{message}\n{grid}")

    def log_grid_operation(self, message: str, grid: 'CellGrid') -> None:
        """Log a grid operation with the current state of the grid."""
        self.log_step(message, grid.render_with_named_nodes()) 

    def log_debug(self, message: str) -> None:
        logging.info(f"[DEBUG] {message}") 