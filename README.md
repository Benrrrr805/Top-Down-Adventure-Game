# Pygame Base Project

This is a boilerplate for a Pygame-based application, structured to let you quickly build 2D games, interactive scenes, and user interface components. The code in this repository is designed with extensibility in mind, allowing you to easily plug in new game logic, scenes, and UI elements.

## Table of Contents
- Overview
- Project Structure
- How to Run
- Adding New Scenes or Game Logic
- Adding New UI Components
- Validation and Debugging
- Known Issues & Recommendations
- License

## Overview

### The core idea is to encapsulate game components into a node-like hierarchy. Each GameComponent can have:

- **Children**: Other GameComponents.
- **Parent**: Another GameComponent (unless it’s top-level).
- **Event handling**: Through an EventQueue.
- **Drawing/Rendering** (if `graphics_enabled = True`).
- **Helper functions**: Additional logic triggered in specific contexts (e.g., `update`, `draw`, `handle_events`).

A main `Game` class acts as the root GameComponent and also manages the main loop (`handle_events`, `update`, `draw`).

## Project Structure

Below is a simplified look at the directory layout mentioned in the code:

```plaintext
.
├─ main.py
├─ assets/
│  ├─ images/
│  ├─ sounds/
│  └─ ...
├─ game/
│  ├─ core/
│  │  ├─ event_queue.py
│  │  ├─ game_loop.py
│  │  └─ game_component.py
│  ├─ entities/
│  │  ├─ uiComponents/
│  │  │  ├─ buttons/
│  │  │  ├─ containers/
│  │  │  └─ menus/
│  ├─ scenes/
│  │  ├─ startingScene.py
│  │  └─ (additional scenes)
│  ├─ utils/
│  │  └─ settings.py
│  └─ settings.py (or equivalent)
└─ README.md
```

### Key Files

- **`main.py`**: The entry point. Instantiates the main `Game` and runs it.

- **`game/core/game_loop.py`**: Contains the `Game` class, which is a special kind of GameComponent responsible for the main loop.

- **`game/core/event_queue.py`**: Defines the EventQueue system for capturing and storing Pygame events in a custom dictionary-based structure.

- **`game/core/game_component.py`**: The foundational class for all interactive items, scenes, or UI elements in the game. Supports:
  - Parenting and child relationships
  - Enabling and disabling
  - Event handling and drawing
  - Helper function system

- **`game/scenes/startingScene.py`**: Example “scene” logic that can display a main menu or other UI components.

- **`game/entities/`**: Placeholder folder for creating classes like Player, Monster, or different interactive objects.

## How to Run

### Install dependencies:

Make sure you have Python 3 and Pygame installed:

```bash
pip install pygame
```

### Run the entry script:

From the project root, run:

```bash
python main.py
```

This will create a window titled “Top-Down Adventure Game,” instantiate the Game object, and enter the main loop.

### Quit:

- Press the ESC key, or
- Close the window by clicking the close button

## Adding New Scenes or Game Logic

### Create a new scene:

1. Make a new file under `game/scenes`, e.g., `myNewScene.py`.
2. Create a class that inherits `GameComponent` (similar to `StartingScene`).
3. Implement `handle_events`, `update`, and `draw`.

### Connect your scene to the Game:

1. Instantiate your new scene in the `Game` class or from `main.py`.
2. Use `GameComponent.link_child(parent, child)` or the convenience methods in `GameComponent` to link.
3. Optionally call `scene.set_scene(self.game)` or similar to pass references.

### Enable your scene:

- Mark it as active (`scene.enable()`).
- Or set it as the current scene in the `Game` class.

## Adding New UI Components

### Create a new UI component:

1. Extend `GameComponent` (or a specialized version) for custom logic.
2. If it’s fully UI-based, set `graphics_enabled = True`.

### Implement `draw()`, `handle_events()`, etc.:

- `draw()` is where you render background, text, or images.
- `handle_events()` uses the injected EventQueue.

### Register the component within a scene:

- Link your component to the scene’s main container or directly to the scene.

### Add helper functions (optional):

- Use `add_helper_function("my_fn_name", my_function, ["update", "handle_events"])`
- This allows your function to run automatically in the specified contexts.

## Validation and Debugging

### Validation

Each `GameComponent` can call `full_validate()` to check:

- Relationship correctness (parent-child).
- Required fields like `name`.
- UI constraints if `graphics_enabled` is True.

### Debugging

- Set `self.debug = True` in a `GameComponent` to toggle debug colors or console logs.
- `self.debug_color` is used for drawing rect borders, toggling between colors on hover, etc.

### Helper Functions

- `run_helper_functions("update")` calls all helper functions that handle the "update" context.
- You can intercept certain events or UI states without mixing them into a single `update()` method.

