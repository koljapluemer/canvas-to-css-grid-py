"""
Convert a CellGrid to an HTML file with CSS grid-template-areas.

The script takes a CellGrid and generates an HTML file where:
1. Each node becomes a named grid area
2. The grid layout matches the CellGrid structure
3. Each node's content is displayed in its grid area
"""

from make_grid_from_json import make_grid_from_json
from cell_grid import CellGrid
import re
import os
def sanitize_area_name(content: str) -> str:
    """Convert node content to a valid CSS grid area name.
    
    CSS grid area names must be valid CSS identifiers.
    We'll convert spaces to hyphens and remove any invalid characters.
    """
    # Replace spaces with hyphens
    name = content.replace(" ", "-")
    # Remove any characters that aren't valid in CSS identifiers
    name = re.sub(r'[^a-zA-Z0-9_-]', '', name)
    # Ensure it starts with a letter
    if not name[0].isalpha():
        name = "area-" + name
    return name

def grid_to_css_grid(grid: CellGrid) -> str:
    """Convert a CellGrid to CSS grid-template-areas string, matching the visual grid."""
    def get_letter_id_for_cell(i, j):
        if grid.cells[i][j] == "node":
            for n in grid.nodes:
                if n.col <= j < n.col + n.width and n.row <= i < n.row + n.height:
                    return n.letter_id
        return "."  # treat all non-node as empty for CSS

    area_rows = []
    for i, row in enumerate(grid.cells):
        area_row = []
        for j, cell in enumerate(row):
            area_row.append(get_letter_id_for_cell(i, j))
        area_rows.append(f'"{' '.join(area_row)}"')
    return "\n            ".join(area_rows)

def generate_html(grid: CellGrid) -> str:
    """Generate an HTML file with CSS grid layout."""
    css_areas = grid_to_css_grid(grid)
    
    # Generate CSS for each node
    node_styles = []
    for node in grid.nodes:
        # Use the node's letter_id for the CSS class
        node_styles.append(f"""
.{node.letter_id} {{
    grid-area: {node.letter_id};
}}""")
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        .grid-container {{
            display: grid;
            grid-template-areas:
            {css_areas};
            gap: 1rem;
            padding: 1rem;
            background: #f5f5f5;
            border-radius: 8px;
        }}
        
        .node {{
            padding: 1rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            font-family: system-ui, -apple-system, sans-serif;
        }}
        
        {chr(10).join(node_styles)}
    </style>
</head>
<body>
    <div class="grid-container">
"""
    
    # Add divs for each node
    for node in grid.nodes:
        html += f'        <div class="node {node.letter_id}">{node.content}</div>\n'
    
    html += """    </div>
</body>
</html>"""
    
    return html

def main():
    # Example usage
    grid_path = "data/json-diagrams/godot_instantiating.canvas" 
    # Create a grid from JSON
    grid = make_grid_from_json(grid_path)
    grid.purge_redundant_columns()
    grid.purge_redundant_rows()
    print(grid.render_with_named_nodes())
    # Generate HTML
    html = generate_html(grid)
    
    # Write to file
    output_dir = "html_output"
    os.makedirs(output_dir, exist_ok=True)
    # grid name is filename without extension and path
    grid_name = os.path.splitext(os.path.basename(grid_path))[0]
    with open(os.path.join(output_dir, f"{grid_name}.html"), "w") as f:
        f.write(html)

if __name__ == "__main__":
    main()
