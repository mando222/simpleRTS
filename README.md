# simpleRTS

A basic Real-Time Strategy (RTS) game engine built with Python and Pygame, featuring an Entity Component System (ECS) architecture.

## Features (Implemented so far)
- Basic Game Loop
- Entity Component System (ECS)
  - Entities, Components (Transform, Sprite, Health, Attack, Movement, Production, Resource, AI)
  - Systems (Render, Input, Combat, AI)
- 2D Rendering (colored rectangles for entities)
- Input Handling (mouse clicks for selection and targeting, basic keyboard input logging)
- Combat Mechanics (units can attack, take damage, and be defeated)
- Basic AI (enemy units can detect, move towards, and attack player units)

## Project Structure
- `assets/`: For game assets (currently unused).
- `ecs/`: Contains the core ECS classes (`entity.py`, `components.py`, `systems.py`).
- `game/`: Contains game-specific logic, including `main.py` (the game entry point), `entities.py` (specialized entity types), `ai_system.py`, and `combat_system.py`.
- `input/`: Contains the `input_system.py`.
- `renderer/`: Contains the `render_system.py`.
- `requirements.txt`: Lists project dependencies.

## Running the Game

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd simpleRTS
    ```

2.  **Set up a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    Make sure you have Python and pip installed. Then, from the project's root directory, run:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the game:**
    Execute the main game file from the project's root directory:
    ```bash
    python game/main.py
    ```

    You should see a Pygame window open, displaying the game entities. You can select your green unit with a left-click and target enemy units with a right-click. AI-controlled enemy units will automatically engage your unit.

## Development
Feel free to extend the engine with new components, systems, and features. Some potential areas for improvement:
- More advanced AI behaviors
- Unit production and resource gathering logic
- Pathfinding
- Sprite-based graphics instead of simple colored rectangles
- UI elements (health bars, resource display, command panel)
- Sound effects and music
- A proper faction/team system for entities