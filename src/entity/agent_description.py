from entity.entity_description import EntityDescription


class AgentDescription(EntityDescription):
    def __init__(self, name, objective_name, start_position=None):
        if objective_name == "":
            raise ValueError("Agent's objective name cannot be empty")

        EntityDescription.__init__(self, name, start_position)
        self._objective_name = objective_name

    def get_objective_name(self):
        return self._objective_name

    def to_dict(self):
        new_dict = super(AgentDescription, self).to_dict()
        new_dict.update({"objective_name": self.get_objective_name()})
        return new_dict

