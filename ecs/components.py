import pygame

class Component:
    pass

class TransformComponent(Component):
    def __init__(self, x=0, y=0, rotation=0, scale_x=1, scale_y=1):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.scale_x = scale_x
        self.scale_y = scale_y

class SpriteComponent(Component):
    def __init__(self, image_path=None, color=None, width=0, height=0):
        self.image = None
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
            except pygame.error as e:
                print(f"Error loading image {image_path}: {e}")
        
        self.color = color # Should be a pygame.Color or tuple (R, G, B)
        self.width = width # Required if no image and color is for a shape
        self.height = height # Required if no image and color is for a shape

        if self.image:
            if width == 0: # if width is not set, use image width
                self.width = self.image.get_width()
            if height == 0: # if height is not set, use image height
                self.height = self.image.get_height()
            
            # if width or height is set, scale the image
            if width !=0 and height !=0 and (width != self.image.get_width() or height != self.image.get_height()):
                self.image = pygame.transform.scale(self.image, (width, height))


        elif color is None:
            # Default to a white square if no image and no color
            self.color = (255, 255, 255)
            if self.width == 0: self.width = 50
            if self.height == 0: self.height = 50

        elif color and (width == 0 or height == 0):
            # If color is provided but no dimensions, default to 50x50
            if self.width == 0: self.width = 50
            if self.height == 0: self.height = 50

# Gameplay Components
class HealthComponent(Component):
    def __init__(self, current_hp, max_hp):
        self.current_hp = current_hp
        self.max_hp = max_hp

class AttackComponent(Component):
    def __init__(self, attack_damage, attack_range, attack_speed):
        self.attack_damage = attack_damage
        self.attack_range = attack_range # e.g., in pixels or game units
        self.attack_speed = attack_speed # e.g., attacks per second

class MovementSpeedComponent(Component):
    def __init__(self, speed):
        self.speed = speed # e.g., pixels per second

class ProductionComponent(Component):
    def __init__(self, unit_types_producible, production_time, queue_limit=5):
        # unit_types_producible could be a list of strings or classes
        self.unit_types_producible = unit_types_producible
        self.production_time = production_time # time in seconds to produce one unit
        self.production_progress = 0
        self.production_queue = []
        self.queue_limit = queue_limit

class ResourceComponent(Component):
    def __init__(self, resource_type, amount):
        self.resource_type = resource_type # e.g., "wood", "gold", "food"
        self.amount = amount

class AIComponent(Component):
    def __init__(self, behavior_type="attack_closest", detection_range=150, ai_team="enemy"):
        self.behavior_type = behavior_type # e.g., "attack_closest", "defend_position", "patrol"
        self.detection_range = detection_range # Max distance to detect enemies
        self.ai_team = ai_team # To distinguish friend from foe (e.g. "player", "enemy")
        # Could add more specific state, like current_target_by_ai, etc.
