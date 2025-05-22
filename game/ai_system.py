import pygame # For math.hypot or vector operations if needed
from ecs.systems import System
from ecs.components import (
    AIComponent, TransformComponent, AttackComponent, 
    MovementSpeedComponent, HealthComponent
)
import math # For distance calculation

class AISystem(System):
    def __init__(self, entities_list_ref):
        super().__init__()
        self.required_component_types = [
            AIComponent, TransformComponent, AttackComponent, 
            MovementSpeedComponent # AI needs to move towards targets
        ]
        self.entities_list_ref = entities_list_ref # Reference to the main list of entities

    def _process_entity(self, ai_entity, dt): # dt is delta time for movement
        ai_comp = ai_entity.get_component(AIComponent)
        ai_transform = ai_entity.get_component(TransformComponent)
        ai_attack = ai_entity.get_component(AttackComponent)
        ai_movement = ai_entity.get_component(MovementSpeedComponent)

        # 1. Target Acquisition Logic
        # Only acquire a new target if the current one is missing, invalid, or defeated
        current_target_valid = False
        if hasattr(ai_attack, 'target_entity') and ai_attack.target_entity is not None:
            if ai_attack.target_entity in self.entities_list_ref and \
               ai_attack.target_entity.has_component(HealthComponent) and \
               ai_attack.target_entity.get_component(HealthComponent).current_hp > 0:
                current_target_valid = True
            else:
                ai_attack.target_entity = None # Clear invalid or defeated target

        if not current_target_valid and ai_comp.behavior_type == "attack_closest":
            closest_target = None
            min_dist_sq = ai_comp.detection_range ** 2

            for potential_target in self.entities_list_ref:
                if potential_target == ai_entity or not potential_target.has_component(HealthComponent):
                    continue # Skip self and entities without health

                # Rudimentary team check: if potential target also has AIComponent, check its team.
                # Otherwise, assume it's a player-controlled unit or a neutral entity that can be attacked.
                is_enemy = True
                if potential_target.has_component(AIComponent):
                    potential_target_ai_comp = potential_target.get_component(AIComponent)
                    if potential_target_ai_comp.ai_team == ai_comp.ai_team:
                        is_enemy = False # Don't target own team members
                
                # For this initial AI, let's assume player units don't have AIComponent,
                # so they are always considered enemies by AI.
                # A more robust team/faction system would be needed for complex scenarios.

                if is_enemy:
                    target_transform = potential_target.get_component(TransformComponent)
                    if not target_transform: continue

                    dist_sq = (ai_transform.x - target_transform.x)**2 + \
                              (ai_transform.y - target_transform.y)**2
                    
                    if dist_sq < min_dist_sq:
                        min_dist_sq = dist_sq
                        closest_target = potential_target
            
            if closest_target:
                ai_attack.target_entity = closest_target
                # print(f"AI Entity {ai_entity.id} acquired target {closest_target.id} at distance {math.sqrt(min_dist_sq):.2f}")


        # 2. Movement Logic (if a target exists and has MovementSpeedComponent)
        if hasattr(ai_attack, 'target_entity') and ai_attack.target_entity is not None:
            target = ai_attack.target_entity
            if target.has_component(TransformComponent): # Ensure target still has transform
                target_transform = target.get_component(TransformComponent)

                dist_x = target_transform.x - ai_transform.x
                dist_y = target_transform.y - ai_transform.y
                distance = math.hypot(dist_x, dist_y)

                # Check if target is outside attack range
                if distance > ai_attack.attack_range:
                    # Move towards target
                    if distance > 0: # Avoid division by zero
                        # Normalize direction vector
                        dir_x = dist_x / distance
                        dir_y = dist_y / distance

                        ai_transform.x += dir_x * ai_movement.speed * dt
                        ai_transform.y += dir_y * ai_movement.speed * dt
                        # print(f"AI Entity {ai_entity.id} moving towards {target.id}. Distance: {distance:.2f}")
                else:
                    # AI is in attack range, CombatSystem will handle attacking
                    # print(f"AI Entity {ai_entity.id} in attack range of {target.id}. CombatSystem will handle.")
                    pass
        # else:
            # print(f"AI Entity {ai_entity.id} has no target or target is invalid.")


    def process(self, entities, dt): # dt needs to be passed from the main loop
        for entity in list(entities): # Iterate over a copy if entities can be removed
            if entity in self.entities_list_ref and all(entity.has_component(ct) for ct in self.required_component_types):
                self._process_entity(entity, dt)
