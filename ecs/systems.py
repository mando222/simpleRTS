class System:
    def __init__(self):
        self.required_component_types = []

    def process(self, entities):
        for entity in entities:
            if all(entity.has_component(ct) for ct in self.required_component_types):
                self._process_entity(entity)

    def _process_entity(self, entity):
        # This method should be overridden by subclasses
        raise NotImplementedError
