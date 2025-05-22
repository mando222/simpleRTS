from ecs.entity import Entity
from ecs.components import (
    TransformComponent, SpriteComponent, HealthComponent, 
    AttackComponent, MovementSpeedComponent, ProductionComponent, 
    ResourceComponent
)

class Unit(Entity):
    def __init__(self, x, y, sprite_color, hp, damage, attack_range, attack_speed, move_speed):
        super().__init__()
        self.add_component(TransformComponent(x=x, y=y))
        self.add_component(SpriteComponent(color=sprite_color, width=30, height=30)) # Default size for units
        self.add_component(HealthComponent(current_hp=hp, max_hp=hp))
        self.add_component(AttackComponent(attack_damage=damage, attack_range=attack_range, attack_speed=attack_speed))
        self.add_component(MovementSpeedComponent(speed=move_speed))
        print(f"Unit created at ({x},{y}) with HP: {hp}, Damage: {damage}")

class Building(Entity):
    def __init__(self, x, y, sprite_color, hp, producible_units, production_time):
        super().__init__()
        self.add_component(TransformComponent(x=x, y=y))
        self.add_component(SpriteComponent(color=sprite_color, width=80, height=80)) # Default size for buildings
        self.add_component(HealthComponent(current_hp=hp, max_hp=hp))
        self.add_component(ProductionComponent(unit_types_producible=producible_units, production_time=production_time))
        print(f"Building created at ({x},{y}) with HP: {hp}, Can produce: {producible_units}")

class Resource(Entity):
    def __init__(self, x, y, sprite_color, resource_type, amount):
        super().__init__()
        self.add_component(TransformComponent(x=x, y=y))
        self.add_component(SpriteComponent(color=sprite_color, width=40, height=40)) # Default size for resources
        self.add_component(ResourceComponent(resource_type=resource_type, amount=amount))
        print(f"Resource node '{resource_type}' created at ({x},{y}) with amount: {amount}")
