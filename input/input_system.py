import pygame
from ecs.systems import System
from ecs.components import TransformComponent, AttackComponent, SpriteComponent # For checking clickable area

class InputSystem(System):
    def __init__(self, entities_list_ref): # Takes a reference to the main entities list
        super().__init__()
        self.entities_list_ref = entities_list_ref
        self.selected_entity = None # To store the currently selected friendly unit
        # No specific components required for this system to act globally on events
        # For now, we'll process global input events.

    def _get_entity_at_pos(self, pos):
        """Helper function to find an entity at a given mouse position."""
        for entity in self.entities_list_ref:
            if entity.has_component(TransformComponent) and entity.has_component(SpriteComponent):
                transform = entity.get_component(TransformComponent)
                sprite = entity.get_component(SpriteComponent)
                
                # Create a rect for the entity based on its position and sprite dimensions
                # Note: This doesn't account for scaling or rotation in sprite component yet for click detection
                # For simplicity, using sprite.width and sprite.height as is.
                entity_rect = pygame.Rect(transform.x, transform.y, sprite.width, sprite.height)
                if entity_rect.collidepoint(pos):
                    return entity
        return None

    def process_events(self, events):
        """
        Process a list of Pygame events.
        This method is called from the main game loop with pygame.event.get().
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                print(f"Key pressed: {pygame.key.name(event.key)}")
                if event.key == pygame.K_ESCAPE: # Deselect entity with ESC
                    if self.selected_entity:
                        print(f"Entity {self.selected_entity.id} deselected.")
                        self.selected_entity = None
            elif event.type == pygame.KEYUP:
                # print(f"Key released: {pygame.key.name(event.key)}")
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_entity = self._get_entity_at_pos(event.pos)

                if event.button == 1: # Left Mouse Button
                    if clicked_entity:
                        # For now, let's assume any entity with AttackComponent can be selected
                        # In a real RTS, you'd check for player ownership
                        if clicked_entity.has_component(AttackComponent):
                            self.selected_entity = clicked_entity
                            print(f"Entity {self.selected_entity.id} selected.")
                        else:
                            if self.selected_entity:
                                print(f"Clicked on non-selectable entity {clicked_entity.id}. Deselecting current unit.")
                                self.selected_entity = None
                            else:
                                print(f"Clicked on non-selectable entity {clicked_entity.id}.")
                    else:
                        if self.selected_entity:
                            print(f"Clicked on empty space. Entity {self.selected_entity.id} deselected.")
                            self.selected_entity = None
                
                elif event.button == 3: # Right Mouse Button
                    if self.selected_entity and self.selected_entity.has_component(AttackComponent):
                        if clicked_entity:
                            # Check if the clicked entity is different from the selected one and can be a target (has Health)
                            if clicked_entity != self.selected_entity and clicked_entity.has_component(HealthComponent):
                                attacker_attack_comp = self.selected_entity.get_component(AttackComponent)
                                attacker_attack_comp.target_entity = clicked_entity
                                print(f"Entity {self.selected_entity.id} targeting Entity {clicked_entity.id}.")
                            elif clicked_entity == self.selected_entity:
                                print(f"Cannot target self.")
                            else:
                                print(f"Entity {clicked_entity.id} cannot be targeted (missing HealthComponent or other criteria).")
                        else:
                            # Right-clicked on empty space, could be for movement command later
                            # For now, clear target if one was set
                            attacker_attack_comp = self.selected_entity.get_component(AttackComponent)
                            if hasattr(attacker_attack_comp, 'target_entity') and attacker_attack_comp.target_entity is not None:
                                print(f"Entity {self.selected_entity.id} cleared target (right-clicked empty space).")
                                attacker_attack_comp.target_entity = None
                    elif self.selected_entity:
                        print(f"Selected entity {self.selected_entity.id} cannot attack.")
                    else:
                        print("Right-clicked but no unit selected.")
            
            # Other event types (MOUSEBUTTONUP, MOUSEMOTION) can be handled similarly if needed
            # For example, MOUSEBUTTONUP:
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     button_name = ""
            #     if event.button == 1: button_name = "Left"
                #     elif event.button == 2: button_name = "Middle"
                #     elif event.button == 3: button_name = "Right"
                #     else: button_name = f"Button {event.button}"
                #     print(f"{button_name} mouse button released at {event.pos}")
                # elif event.type == pygame.MOUSEMOTION:
                #     # Optionally handle mouse motion
                #     # print(f"Mouse moved to {event.pos} with buttons {event.buttons}")
                #     pass

    def process(self, entities): # 'entities' parameter is kept for consistency with System base class
        # The main work of this system is event-driven in process_events.
        # Continuous input (keys held down) can be processed here if needed.
        # For example, moving a selected unit with arrow keys:
        # if self.selected_entity and self.selected_entity.has_component(TransformComponent) and self.selected_entity.has_component(MovementSpeedComponent):
        #     keys = pygame.key.get_pressed()
        #     transform = self.selected_entity.get_component(TransformComponent)
        #     speed = self.selected_entity.get_component(MovementSpeedComponent).speed
        #     # dt would be needed here if used for movement
        #     if keys[pygame.K_LEFT]:
        #         transform.x -= speed * (dt or 0.016) # Assuming dt if available, else fallback
        #     if keys[pygame.K_RIGHT]:
        #         transform.x += speed * (dt or 0.016)
        #     if keys[pygame.K_UP]:
        #         transform.y -= speed * (dt or 0.016)
        #     if keys[pygame.K_DOWN]:
        #         transform.y += speed * (dt or 0.016)
        pass # dt is not passed to this process method in the current main loop structure.

    # Note: This system's `_process_entity` method is not used as it doesn't
    # iterate over entities based on components in the same way RenderSystem does.
    # Its primary interaction is through the `process_events` method.
