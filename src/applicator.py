import yaml
import subprocess
from wayfire_ipc import WayfireIPC

class ConfigApplicator:
    def __init__(self, config_path):
        self.config_path = config_path
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.ipc = WayfireIPC()

    def apply(self):
        if 'autostart' in self.config:
            self.run_autostart(self.config['autostart'])
        
        if 'outputs' in self.config:
            self.apply_outputs(self.config['outputs'])
            
        if 'rules' in self.config:
            self.apply_rules(self.config['rules'])

    def run_autostart(self, apps):
        for app in apps:
            print(f"Starting {app}...")
            subprocess.Popen(app.split(), start_new_session=True)

    def apply_outputs(self, outputs):
        print("Applying output configuration...")
        for name, cfg in outputs.items():
            section = f"output:{name}"
            for option, value in cfg.items():
                print(f"  Setting {section}/{option} = {value}")
                self.ipc.set_config_option(section, option, str(value))

    def apply_rules(self, rules):
        views = self.ipc.list_views()
        for rule in rules:
            match = rule.get('match', {})
            action = rule.get('action', {})
            
            for view in views:
                if self._match_view(view, match):
                    self._apply_action(view, action)

    def _match_view(self, view, match):
        for key, value in match.items():
            if getattr(view, key, None) != value:
                return False
        return True

    def _apply_action(self, view, action):
        print(f"Applying action to {view.app_id} ({view.id}): {action}")
        
        try:
            if 'sticky' in action:
                self.ipc.set_view_sticky(view.id, action['sticky'])
            
            if 'maximize' in action:
                if action['maximize']:
                    self.ipc.set_view_fullscreen(view.id, True)
                else:
                    self.ipc.set_view_fullscreen(view.id, False)

            if 'fullscreen' in action:
                self.ipc.set_view_fullscreen(view.id, action['fullscreen'])

            if 'minimized' in action:
                self.ipc.set_view_minimized(view.id, action['minimized'])

            if 'output' in action:
                # Move to output by name or id
                outputs = self.ipc.list_outputs()
                target_output = next((o for o in outputs if o.name == action['output'] or str(o.id) == str(action['output'])), None)
                if target_output:
                    print(f"  Moving to output {target_output.name} (wset {target_output.wset_index})")
                    self.ipc.socket.send_view_to_wset(view.id, target_output.wset_index)
            
            if 'set_workspace' in action:
                target_ws = action['set_workspace']
                # Determine target x, y
                target_x, target_y = 0, 0
                
                # We need the grid dimensions of the view's current wset
                wsets = self.ipc.list_wsets()
                current_wset = next((w for w in wsets if w.index == view.wset_index), None)
                
                if current_wset:
                    grid_width = current_wset.workspace.grid_width
                    # grid_height = current_wset.workspace.grid_height
                    
                    if isinstance(target_ws, int):
                        target_x = target_ws % grid_width
                        target_y = target_ws // grid_width
                    elif isinstance(target_ws, (list, tuple)) and len(target_ws) == 2:
                        target_x, target_y = target_ws
                    elif isinstance(target_ws, str) and ',' in target_ws:
                        parts = target_ws.split(',')
                        target_x, target_y = int(parts[0]), int(parts[1])
                    
                    print(f"  Moving to workspace {target_x},{target_y}")
                    self.ipc.set_workspace(target_x, target_y, view_id=view.id)
                else:
                    print(f"  Warning: Could not find wset {view.wset_index} for view {view.id}")

        except Exception as e:
            print(f"  Error applying action to view {view.id}: {e}")

    def watch_events(self):
        print("Watching for events...")
        self.ipc.socket.watch(['view-mapped'])
        while True:
            event = self.ipc.socket.read_next_event()
            if not event:
                continue
            
            if event.get('event') == 'view-mapped':
                view_data = event.get('view')
                if view_data:
                    from view import View
                    view = View.new(**view_data)
                    print(f"New view mapped: {view.app_id} ({view.id})")
                    for rule in self.config.get('rules', []):
                        if self._match_view(view, rule.get('match', {})):
                            self._apply_action(view, rule.get('action', {}))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        applicator = ConfigApplicator(sys.argv[1])
        applicator.apply()
