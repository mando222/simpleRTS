import sys
import os

# Get the absolute path of the directory containing main.py (game/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the absolute path of the project root directory (one level up from game/)
project_root = os.path.dirname(current_dir)
# Add the project root to sys.path
sys.path.insert(0, project_root)

import pygame
from ecs.entity import Entity # Though we might not directly use Entity if we use specialized classes
from ecs.components import (
    TransformComponent, SpriteComponent, HealthComponent, 
    AttackComponent, MovementSpeedComponent, ProductionComponent, 
    ResourceComponent, HealthComponent, AIComponent # Make sure AIComponent is imported
)
from renderer.render_system import RenderSystem
from input.input_system import InputSystem
from game.entities import Unit, Building, Resource # Import new entity classes
from game.combat_system import CombatSystem # Import CombatSystem
from game.ai_system import AISystem # Import AISystem

def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Engine")

    entities = [] # This will be the main list of all entities
    render_system = RenderSystem(screen)
    input_system = InputSystem(entities) # Pass entities list to InputSystem
    combat_system = CombatSystem(entities) # Pass entities list to CombatSystem
    ai_system = AISystem(entities) # Pass entities list to AISystem

    # Create instances of new entity classes
    # Unit: x, y, sprite_color, hp, damage, attack_range, attack_speed, move_speed
    player_unit = Unit(x=100, y=100, sprite_color=(0, 255, 0), hp=100, damage=10, attack_range=70, attack_speed=1, move_speed=60)
    # Optionally, give player unit a "team" if AI needs to distinguish it more explicitly
    # player_unit.add_component(AIComponent(ai_team="player_team", detection_range=0)) # detection_range=0 for non-aggressive AI
    entities.append(player_unit)

    enemy_unit = Unit(x=300, y=150, sprite_color=(255, 0, 0), hp=80, damage=8, attack_range=60, attack_speed=0.8, move_speed=50)
    enemy_unit.add_component(AIComponent(behavior_type="attack_closest", detection_range=200, ai_team="enemy_team_1"))
    entities.append(enemy_unit)
    
    # Add another enemy unit for more complex scenarios
    enemy_unit_2 = Unit(x=350, y=100, sprite_color=(255, 100, 0), hp=60, damage=5, attack_range=50, attack_speed=1.2, move_speed=70)
    enemy_unit_2.add_component(AIComponent(behavior_type="attack_closest", detection_range=180, ai_team="enemy_team_1"))
    entities.append(enemy_unit_2)
    
    # Add a third enemy unit on a different AI team to test AI team logic (should not attack other enemies on same team)
    enemy_unit_3 = Unit(x=450, y=200, sprite_color=(200, 0, 200), hp=70, damage=7, attack_range=55, attack_speed=0.9, move_speed=40)
    enemy_unit_3.add_component(AIComponent(behavior_type="attack_closest", detection_range=190, ai_team="enemy_team_2")) # Different team
    entities.append(enemy_unit_3)


    # Building: x, y, sprite_color, hp, producible_units, production_time
    player_barracks = Building(x=50, y=300, sprite_color=(0, 0, 255), hp=500, producible_units=["swordsman", "archer"], production_time=10)
    entities.append(player_barracks)

    # Resource: x, y, sprite_color, resource_type, amount
    gold_mine = Resource(x=400, y=400, sprite_color=(255, 215, 0), resource_type="gold", amount=1000)
    entities.append(gold_mine)

    tree = Resource(x=500, y=100, sprite_color=(34, 139, 34), resource_type="wood", amount=500)
    entities.append(tree)
    

    running = True
    clock = pygame.time.Clock() # Add a clock for controlling FPS

    while running:
        dt = clock.tick(60) / 1000.0 # Delta time in seconds

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        input_system.process_events(events) # Process discrete input events

        # Update game logic here (e.g., modify components)
        # REMOVE automatic movement for player_unit to test combat
        # player_unit_transform = player_unit.get_component(TransformComponent)
        # player_unit_speed = player_unit.get_component(MovementSpeedComponent)
        # if player_unit_transform and player_unit_speed:
        #     player_unit_transform.x += player_unit_speed.speed * dt 
        #     if player_unit_transform.x > screen_width:
        #         player_unit_transform.x = 0 # Reset position if it goes off screen
        
        # Update systems
        ai_system.process(entities, dt)    # Process AI logic (target acquisition, movement)
        combat_system.update_cooldowns(dt) # Update attack cooldowns
        combat_system.process(entities)    # Process attacks (both player and AI)

        # Process continuous input (like keys being held down)
        # Pass dt for potential movement logic inside input_system.process if implemented
        input_system.process(entities) 

        # Render graphics here
        screen.fill((20, 20, 20))  # Slightly lighter background
        render_system.process(entities) # Process and draw all entities
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
