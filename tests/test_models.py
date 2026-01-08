import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from view import View, ViewData
from outputs import Output, OutputData
from workspace import WSet, WSetData

class TestModels(unittest.TestCase):
    def test_view_creation(self):
        data = {
            'id': 1,
            'app-id': 'test-app',
            'title': 'Test Window',
            'geometry': {'x': 0, 'y': 0, 'width': 100, 'height': 100},
            'unknown-field': 'should-be-ignored'
        }
        view = View.new(**data)
        self.assertIsInstance(view, ViewData)
        self.assertEqual(view.id, 1)
        self.assertEqual(view.app_id, 'test-app')
        # Ensure unknown fields didn't crash it and aren't in the object (dataclasses are fixed)
        self.assertFalse(hasattr(view, 'unknown_field'))

    def test_output_creation(self):
        data = {
            'id': 1,
            'name': 'HDMI-1',
            'wset-index': 2,
            'workspace': {'grid_width': 3, 'grid_height': 3}
        }
        output = Output.new(**data)
        self.assertIsInstance(output, OutputData)
        self.assertEqual(output.wset_index, 2)
        self.assertEqual(output.workspace.grid_width, 3)

    def test_wset_creation(self):
        data = {
            'index': 1,
            'output-name': 'HDMI-1',
            'output-id': 5
        }
        wset = WSet.new(**data)
        self.assertIsInstance(wset, WSetData)
        self.assertEqual(wset.output_name, 'HDMI-1')
        self.assertEqual(wset.output_id, 5)

if __name__ == '__main__':
    unittest.main()
