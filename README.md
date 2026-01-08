# Wayfire Desktop Configuration Manager

A Python-based utility to declaratively configure the Wayfire desktop environment. It allows you to define your desired output settings, autostart applications, and window rules in a simple YAML file.

## Features

- **Declarative Configuration**: Manage your desktop layout with a single `config.yaml` file.
- **Output Management**: Configure resolution, position, scale, and transform for your monitors.
- **Window Rules**: Automatically move windows to specific outputs or workspaces, maximize them, or make them sticky based on their App ID.
- **Daemon Mode**: Run in the background to apply rules instantly as new windows are opened.

## Requirements

- Python 3
- `wayfire` python module (usually provided by `wayfire` package or installed via pip)
- `pyyaml`

## Installation

1. Clone this repository.
2. Ensure you have the dependencies.
   ```bash
   pip install pyyaml
   # If wayfire python bindings are not in your path, you might need to set PYTHONPATH
   ```

## Usage

### 1. Create a Configuration File

Create a `config.yaml` file. Example:

```yaml
# Autostart applications
autostart:
  - kitty
  - firefox

# Output configuration
outputs:
  HDMI-A-1:
    mode: "2560x1440@60"
    position: "0,0"
    scale: 1.0
  DP-1:
    mode: "1920x1080@60"
    position: "2560,0"

# Window rules
rules:
  - match:
      app_id: "firefox"
    action:
      output: "HDMI-A-1"
      maximize: true
  - match:
      app_id: "kitty"
    action:
      output: "DP-1"
      set_workspace: 1 # Linear index (depends on grid size)
      sticky: false
```

### 2. Run the Manager

To apply the configuration once:

```bash
./wayfire-config-manager.py --config config.yaml --apply
```

To run as a daemon (continuously applying rules):

```bash
./wayfire-config-manager.py --config config.yaml --daemon
```

## Structure

- `wayfire-config-manager.py`: Main entry point.
- `src/`:
    - `applicator.py`: Logic for applying configurations.
    - `view.py`, `outputs.py`, `workspace.py`: Data structures wrapping Wayfire IPC.
    - `wayfire_ipc.py`: Service layer for IPC communication.

## Troubleshooting

If you encounter `ModuleNotFoundError: No module named 'wayfire'`, you need to find where the `wayfire` python package is installed and add it to your `PYTHONPATH`.

Example:
```bash
export PYTHONPATH=$PYTHONPATH:/usr/lib/python3.13/site-packages
./wayfire-config-manager.py ...
```
