from entity.entity_description import EntityDescription


class AgentDescription(EntityDescription):
    def __init__(self, name, start_position=None, objective=None):
        if not objective:
            raise ValueError("Objective of the agent must be declared")

        EntityDescription.__init__(self, name, start_position)
        self._objective = objective

    def get_objective(self):
        return self._objective

