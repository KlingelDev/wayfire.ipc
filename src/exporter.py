import yaml
from wayfire_ipc import WayfireIPC

class ConfigExporter:
    def __init__(self):
        self.ipc = WayfireIPC()

    def export(self, output_path):
        config = {
            'outputs': self._get_outputs(),
            'rules': self._get_rules(),
            'workspaces': self._get_workspaces()
        }
        
        with open(output_path, 'w') as f:
            yaml.dump(config, f, sort_keys=False)
        print(f"Configuration saved to {output_path}")

    def _get_outputs(self):
        outputs_cfg = {}
        for output in self.ipc.list_outputs():
            outputs_cfg[output.name] = {
                'mode': f"{output.geometry['width']}x{output.geometry['height']}",
                'position': f"{output.geometry['x']},{output.geometry['y']}"
            }
        return outputs_cfg

    def _get_rules(self):
        rules = []
        views = self.ipc.list_views()
        for view in views:
            if not view.app_id:
                continue
                
            rule = {
                'match': {
                    'app_id': view.app_id
                },
                'action': {
                    'output': view.output_name,
                    'maximize': view.fullscreen,
                    'sticky': view.sticky,
                    'geometry': {
                        'x': view.geometry['x'],
                        'y': view.geometry['y'],
                        'width': view.geometry['width'],
                        'height': view.geometry['height']
                    }
                }
            }
            # Only add if it's not already covered by a similar rule for the same app_id
            if rule not in rules:
                rules.append(rule)
        return rules

    def _get_workspaces(self):
        # Just use the first output's grid as a template
        outputs = self.ipc.list_outputs()
        if outputs:
            return {
                'grid': {
                    'width': outputs[0].workspace.grid_width,
                    'height': outputs[0].workspace.grid_height
                }
            }
        return {}
