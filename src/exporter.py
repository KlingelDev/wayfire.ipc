import yaml
from wayfire_ipc import WayfireIPC

class ConfigExporter:
    def __init__(self):
        self.ipc = WayfireIPC()

    def export(self, output_path):
        self.view_ws_map = self._map_views_to_workspaces()
        
        config = {
            'outputs': self._get_outputs(),
            'rules': self._get_rules(),
            'workspaces': self._get_workspaces()
        }
        
        with open(output_path, 'w') as f:
            yaml.dump(config, f, sort_keys=False)
        print(f"Configuration saved to {output_path}")

    def _map_views_to_workspaces(self):
        view_map = {}
        wsets = self.ipc.list_wsets()
        outputs = self.ipc.list_outputs()

        # Method 1: Tiling Layout Scan
        for wset in wsets:
            output = next((o for o in outputs if o.wset_index == wset.index), None)
            if not output: continue

            gw = output.workspace.grid_width
            gh = output.workspace.grid_height

            for x in range(gw):
                for y in range(gh):
                    try:
                        layout = self.ipc.socket.get_tiling_layout(wset.index, x, y)
                        ids = self._extract_ids(layout)
                        for vid in ids:
                            view_map[vid] = (x, y)
                    except:
                        pass
        return view_map

    def _extract_ids(self, node):
        ids = []
        if isinstance(node, dict):
            if 'view-id' in node:
                ids.append(node['view-id'])
            for key in ['nodes', 'horizontal-split', 'vertical-split']:
                if key in node:
                    for child in node[key]:
                        ids.extend(self._extract_ids(child))
        return ids

    def _get_outputs(self):
        outputs_cfg = {}
        for output in self.ipc.list_outputs():
            outputs_cfg[output.name] = {
                'mode': f"{output.geometry['width']}x{output.geometry['height']}",
                'position': f"{output.geometry['x']},{output.geometry['y']}",
                'scale': 1.0 # Default, could fetch if available
            }
        return outputs_cfg

    def _get_rules(self):
        rules = []
        views = self.ipc.list_views()
        outputs = self.ipc.list_outputs()

        for view in views:
            if not view.app_id:
                continue
            
            # Determine Workspace
            ws = self.view_ws_map.get(view.id)
            if not ws:
                # Fallback: Coordinate based
                # Find the output this view is on
                output = next((o for o in outputs if o.name == view.output_name), None)
                if output:
                    # In Wayfire, view geometry is usually relative to the workspace if it's active?
                    # Or global?
                    # Assuming global output coordinates for now.
                    # Actually, if we couldn't find it in tiling layout, it might be floating.
                    # We'll omit workspace if we can't be sure, to avoid errors.
                    pass

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
            
            if ws:
                rule['action']['set_workspace'] = f"{ws[0]},{ws[1]}"

            # Check for duplicates (simplified)
            # We want to keep unique rules per app instance if geometries differ
            # But the user might want a generic rule. 
            # For a snapshot, we want exact restoration, so we keep all.
            # However, if app_ids are identical, Applicator will match the first rule it finds 
            # for ALL windows with that app_id, which is bad for multiple instances.
            # This is a limitation of the current simple matching logic.
            # TODO: Add title matching or more specific matching if needed.
            # For now, we append.
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
