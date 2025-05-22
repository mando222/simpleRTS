import pygame
from ecs.systems import System
from ecs.components import TransformComponent, SpriteComponent

class RenderSystem(System):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.required_component_types = [TransformComponent, SpriteComponent]

    def _process_entity(self, entity):
        transform = entity.get_component(TransformComponent)
        sprite = entity.get_component(SpriteComponent)

        if sprite.image:
            # Create a copy of the original image to avoid modifying it directly
            image_to_render = sprite.image.copy()
            
            # Scale
            scaled_image = pygame.transform.scale(image_to_render, (int(sprite.width * transform.scale_x), int(sprite.height * transform.scale_y)))
            
            # Rotate
            # For rotation, it's often better to rotate around the center.
            # Pygame's transform.rotate rotates around the top-left corner.
            # To rotate around the center, we need a more complex operation or adjust position after rotation.
            # For simplicity here, we'll rotate around the top-left.
            rotated_image = pygame.transform.rotate(scaled_image, transform.rotation)
            
            # Get the rect of the rotated image to position it correctly
            rect = rotated_image.get_rect()
            rect.x = transform.x
            rect.y = transform.y
            
            self.screen.blit(rotated_image, rect)

        elif sprite.color:
            # Draw a rectangle if there's a color but no image
            rect = pygame.Rect(transform.x, transform.y, 
                               int(sprite.width * transform.scale_x), 
                               int(sprite.height * transform.scale_y))
            pygame.draw.rect(self.screen, sprite.color, rect)
        
        # Note: This basic renderer does not handle camera, layers, or advanced sprite effects.
        # Rotation is also simplified (around top-left). Proper centered rotation requires more steps.
