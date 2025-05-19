import os
import unittest
from utils.read_plaintext_to_model.ingest import ingest

class TestAdvancedDiagram(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(self.test_dir, 'in.txt'), 'r') as f:
            self.input_text = f.read()
        with open(os.path.join(self.test_dir, 'out.txt'), 'r') as f:
            self.expected_output = f.read()

    def test_ingest(self):
        # Run the ingest function
        meta_grid, grid = ingest(self.input_text)
        
        # Test MetaGrid structure
        self.assertEqual(len(meta_grid.nodes), 2, "Should have 2 nodes")
        node_contents = {node.content for node in meta_grid.nodes}
        self.assertEqual(node_contents, {'a', 'b'}, "Should have nodes 'a' and 'b'")
        
        self.assertEqual(len(meta_grid.edges), 1, "Should have 1 edge")
        edge = meta_grid.edges[0]
        self.assertEqual(edge.origin.content, 'a', "Edge should start from 'a'")
        self.assertEqual(edge.destination.content, 'b', "Edge should end at 'b'")
        self.assertTrue(edge.hasArrowAtDestination, "Edge should have arrow at destination")
        self.assertFalse(edge.hasArrowAtOrigin, "Edge should not have arrow at origin")
        
        # Test Grid rendering
        rendered_output = grid.render()
        self.assertEqual(rendered_output, self.expected_output, 
                        "Rendered output should match expected output")

if __name__ == '__main__':
    unittest.main()
