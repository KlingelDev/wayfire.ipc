#!/usr/bin/env python3

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from wayfire import WayfireSocket
from view import View
from outputs import Output
from workspace import WSet

class WayfireIPC:
    def __init__(self):
        # Let the caller handle connection errors
        self.socket = WayfireSocket()

    def list_views(self):
        try:
            return [View.new(**v) for v in self.socket.list_views()]
        except Exception as e:
            print(f"Error listing views: {e}")
            return []

    def list_outputs(self):
        try:
            return [Output.new(**o) for o in self.socket.list_outputs()]
        except Exception as e:
            print(f"Error listing outputs: {e}")
            return []

    def list_wsets(self):
        try:
            return [WSet.new(**w) for w in self.socket.list_wsets()]
        except Exception as e:
            print(f"Error listing wsets: {e}")
            return []

    def set_view_sticky(self, view_id: int, sticky: bool):
        try:
            return self.socket.set_view_sticky(view_id, sticky)
        except Exception as e:
            print(f"Error setting sticky for view {view_id}: {e}")

    def set_view_fullscreen(self, view_id: int, fullscreen: bool):
        try:
            return self.socket.set_view_fullscreen(view_id, fullscreen)
        except Exception as e:
            print(f"Error setting fullscreen for view {view_id}: {e}")

    def set_view_minimized(self, view_id: int, minimized: bool):
        try:
            return self.socket.set_view_minimized(view_id, minimized)
        except Exception as e:
            print(f"Error setting minimized for view {view_id}: {e}")

    def set_config_option(self, section: str, option: str, value: any):
        try:
            return self.socket.set_option_values({f"{section}/{option}": value})
        except Exception as e:
            print(f"Error setting config option {section}/{option}: {e}")

    def set_workspace(self, workspace_x: int, workspace_y: int, view_id: int = None, output_id: int = None):
        try:
            return self.socket.set_workspace(workspace_x, workspace_y, view_id, output_id)
        except Exception as e:
            print(f"Error setting workspace: {e}")

def run() -> int:
    ipc = WayfireIPC()

    print("--- Views ---")
    for v in ipc.list_views():
        print(f"{v.id}: {v.app_id} - {v.title}")

    print("\n--- Outputs ---")
    for o in ipc.list_outputs():
        print(f"{o.id}: {o.name} ({o.geometry['width']}x{o.geometry['height']})")

    print("\n--- WSets ---")
    for w in ipc.list_wsets():
        print(f"{w.index}: {w.name} on {w.output_name}")

    return 0

if __name__ == '__main__':
    # Ensure we use the correct PYTHONPATH if needed, or just run it.
    # Note: In this environment, we found we need a specific PYTHONPATH.
    run()