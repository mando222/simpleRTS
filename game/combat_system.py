import pygame # For potential use with range calculations or effects later
from ecs.systems import System
from ecs.components import TransformComponent, AttackComponent, HealthComponent

class CombatSystem(System):
    def __init__(self, entities_list_ref):
        super().__init__()
        self.required_component_types = [AttackComponent, TransformComponent] # Attacker needs these
        # HealthComponent is checked on the target, not required for the attacker itself
        self.entities_list_ref = entities_list_ref # Direct reference to the main list of entities

    def _process_entity(self, entity):
        attacker_attack_comp = entity.get_component(AttackComponent)
        attacker_transform_comp = entity.get_component(TransformComponent)

        # Check if the attacker has a target
        if not hasattr(attacker_attack_comp, 'target_entity') or attacker_attack_comp.target_entity is None:
            return # No target, nothing to do for this entity

        target = attacker_attack_comp.target_entity
        
        # Validate target still exists and has necessary components
        if target not in self.entities_list_ref or not target.has_component(HealthComponent) or not target.has_component(TransformComponent):
            attacker_attack_comp.target_entity = None # Clear invalid target
            return

        target_health_comp = target.get_component(HealthComponent)
        target_transform_comp = target.get_component(TransformComponent)

        # Calculate distance (simple Euclidean distance)
        distance_sq = (attacker_transform_comp.x - target_transform_comp.x)**2 + \
                      (attacker_transform_comp.y - target_transform_comp.y)**2
        attack_range_sq = attacker_attack_comp.attack_range**2

        if distance_sq <= attack_range_sq:
            # Attacker is in range, process attack
            # Implement attack cooldown/speed
            if not hasattr(attacker_attack_comp, 'attack_cooldown'):
                attacker_attack_comp.attack_cooldown = 0.0
            
            if attacker_attack_comp.attack_cooldown <= 0.0:
                print(f"Entity {entity.id} attacks Entity {target.id} for {attacker_attack_comp.attack_damage} damage.")
                target_health_comp.current_hp -= attacker_attack_comp.attack_damage
                print(f"Entity {target.id} health is now {target_health_comp.current_hp}/{target_health_comp.max_hp}")

                if target_health_comp.current_hp <= 0:
                    print(f"Entity {target.id} has been defeated.")
                    self.entities_list_ref.remove(target)
                    attacker_attack_comp.target_entity = None # Clear target after defeat
                
                # Reset cooldown based on attack speed (attacks per second)
                attacker_attack_comp.attack_cooldown = 1.0 / attacker_attack_comp.attack_speed
            else:
                # Cooldown is active, handled in the main loop's dt update
                pass 
        else:
            # Target is out of range. For now, do nothing.
            # Later, units might move towards their target if out of range.
            # print(f"Entity {entity.id} target {target.id} is out of range.")
            pass

    def update_cooldowns(self, dt):
        # This method needs to be called each frame from the main loop
        for entity in self.entities_list_ref: # Iterate over all entities to find attackers
            if entity.has_component(AttackComponent):
                attack_comp = entity.get_component(AttackComponent)
                if hasattr(attack_comp, 'attack_cooldown') and attack_comp.attack_cooldown > 0:
                    attack_comp.attack_cooldown -= dt
                    if attack_comp.attack_cooldown < 0:
                        attack_comp.attack_cooldown = 0.0
                        
    # Overriding process to use the potentially modified entities_list_ref
    def process(self, entities): # 'entities' here is the main list from game loop
        # Update cooldowns first
        # self.update_cooldowns(dt) # dt needs to be passed or accessed

        # Process attacks for entities that can attack
        # Iterate over a copy if entities can be removed during processing
        for entity in list(entities): 
            if entity in self.entities_list_ref and all(entity.has_component(ct) for ct in self.required_component_types):
                self._process_entity(entity)
