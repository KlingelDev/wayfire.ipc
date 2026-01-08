import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock the wayfire module BEFORE importing applicator
sys.modules['wayfire'] = MagicMock()
from wayfire import WayfireSocket

from applicator import ConfigApplicator
from view import ViewData
from outputs import OutputData
from workspace import WSetData, WorkspaceData

class TestApplicator(unittest.TestCase):
    def setUp(self):
        # Create a dummy config file
        with open('test_config.yaml', 'w') as f:
            f.write("""
rules:
  - match:
      app_id: "test_app"
    action:
      maximize: true
      sticky: true
      output: "HDMI-1"
      set_workspace: 5
""")
        
        # Mock the IPC
        self.mock_socket = MagicMock()
        with patch('wayfire_ipc.WayfireSocket', return_value=self.mock_socket):
            self.applicator = ConfigApplicator('test_config.yaml')
            # Inject the mock socket directly into the ipc wrapper to be sure
            self.applicator.ipc.socket = self.mock_socket

    def tearDown(self):
        if os.path.exists('test_config.yaml'):
            os.remove('test_config.yaml')

    def test_apply_rules(self):
        # Setup mock data
        view = ViewData(id=1, app_id="test_app", wset_index=1)
        output = OutputData(id=10, name="HDMI-1", wset_index=2)
        wset = WSetData(index=1, workspace=WorkspaceData(grid_width=3, grid_height=3))
        
        # Mock IPC responses
        self.applicator.ipc.list_views = MagicMock(return_value=[view])
        self.applicator.ipc.list_outputs = MagicMock(return_value=[output])
        self.applicator.ipc.list_wsets = MagicMock(return_value=[wset])

        # Run apply
        self.applicator.apply_rules(self.applicator.config['rules'])

        # Check calls
        self.mock_socket.set_view_fullscreen.assert_called_with(1, True)
        self.mock_socket.set_view_sticky.assert_called_with(1, True)
        self.mock_socket.send_view_to_wset.assert_called_with(1, 2) # Moved to HDMI-1's wset
        self.mock_socket.set_workspace.assert_called_with(2, 1, 1, None) # Workspace 5 -> (2, 1) in 3x3 grid

if __name__ == '__main__':
    unittest.main()
