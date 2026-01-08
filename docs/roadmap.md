# Wayfire IPC Desktop Configuration Roadmap

## Project Goal
Create a Python-based utility to configure the Wayfire desktop environment declaratively using a configuration file. This tool will interface with Wayfire via its IPC socket to apply settings for outputs, workspaces, and window rules.

## Roadmap

### Phase 1: Foundation & API Wrappers
*Objective: Create robust, type-safe Python wrappers around the raw Wayfire IPC data.*

- [x] **Data Structures**: Implement dataclasses in `src/` to represent Wayfire entities.
    - [x] `src/view.py`: Refine `View` and `ViewData`.
    - [x] `src/outputs.py`: Implement `Output` class.
    - [x] `src/workspace.py`: Implement `Workspace` and `WSet` classes.
- [x] **IPC Abstraction**: Create a service layer (`wayfire_ipc.py`) that uses `WayfireSocket`.
- [x] **Typing**: Ensure full type hinting for better developer experience.

### Phase 2: Configuration Design
*Objective: Define a human-readable configuration format.*

- [x] **Format Selection**: YAML.
- [x] **Schema Definition**: Defined schema for Autostart, Outputs, and Window Rules.
- [x] **Config Parser**: Implemented in `src/applicator.py`.

### Phase 3: Logic Engine (The "Applicator")
*Objective: Implement the logic to transition the desktop from the current state to the desired state.*

- [ ] **State Diffing**: (Optional)
- [x] **Action Executors**:
    - [x] **Output Configurator**: Sets Wayfire config options via IPC.
    - [x] **Layout Manager**: Implemented `set_workspace` and output moving logic.
    - [x] **Rule Matcher**: Scans existing views and applies rules.
- [x] **Event Listener**: Daemon mode implemented in `src/applicator.py`.

### Phase 4: CLI & Polish
*Objective: User interface and distribution.*

- [x] **CLI Entry Point**: `wayfire-config-manager.py` with `--apply` and `--daemon` flags.
- [x] **Documentation**: Usage guide in `README.md`.
- [x] **Error Handling**: Added try-except blocks in `wayfire_ipc.py` and `src/applicator.py`.

## Current Status
- `wayfire_ipc.py`: Basic script connecting to socket.
- `src/view.py`: Initial `ViewData` dataclass.
- `src/outputs.py`: Empty.
- `src/workspace.py`: Empty.
