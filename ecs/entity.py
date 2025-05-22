import uuid

class Entity:
    def __init__(self):
        self.id = uuid.uuid4()
        self._components = {}

    def add_component(self, component):
        component_type = type(component)
        self._components[component_type] = component

    def get_component(self, component_type):
        return self._components.get(component_type)

    def has_component(self, component_type):
        return component_type in self._components

    def remove_component(self, component_type):
        if component_type in self._components:
            del self._components[component_type]
