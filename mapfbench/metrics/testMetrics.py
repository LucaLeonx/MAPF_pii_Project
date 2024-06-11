from result.action import Action
from result.testrun import TestRun
from metrics.agentMetrics import AgentMetrics


# TODO
# -Distanza complessiva
# -altri
# Per test:
# -% successi
# -makespan medio/minimo
# Metric
# -Convert to CSV in Output

class Collision:
    def __init__(self, timestep: int, entity1: str, entity2: str, type: str):
        self._timestep = timestep
        self._entity1 = entity1
        self._entity2 = entity2
        self._collType = type

    @property
    def collision_type(self) -> str:
        return self._collType

    @property
    def timestep(self) -> int:
        return self._timestep

    @property
    def entity1(self) -> str:
        return self._entity1

    @property
    def entity2(self) -> str:
        return self._entity2

    def to_dict(self):
        return {
            "Collision type": self._collType,
            "timestep": self._timestep,
            "Agent 1": self._entity1,
            "Agent 2": self._entity2
        }

    def __str__(self) -> str:
        return "Collision timestep: " + str(self._timestep) + " | between " + self._entity1 + " and " + self._entity2


class TestMetrics:
    def __init__(self, testRun: TestRun):
        self.testReference = testRun
        self.collisions: list[Collision] = []
        self.agentMetricsList: list[AgentMetrics] = []
        self.actionsWithoutAgent = self.testReference.action_list
        self._agents_num = len(self.testReference.agents)
        for agent in self.testReference.agents:
            agentMetric = AgentMetrics(agent, self.take_actions_by_agent(agent.name))
            self.agentMetricsList.append(agentMetric)
        self.evaluate()

    def take_actions_by_agent(self, agentName) -> list[Action]:
        return [action for action in self.actionsWithoutAgent if action.subject == agentName]

    def evaluate_make_span(self):
        self.makeSpan = max([agentMetrics.timeToReachTarget for agentMetrics in self.agentMetricsList])

    def evaluate_sum_of_costs(self):
        self.sumOfCosts = sum([agentMetrics.timeToReachTarget for agentMetrics in self.agentMetricsList])

    def evaluate_medium_costs(self):
        self.mediumCost = sum([agentMetrics.timeToReachTarget for agentMetrics in
                               self.agentMetricsList]) / self._agents_num

    def catch_conflicts(self) -> list[Collision]:
        actionList = self.testReference.action_list
        moveActionList = [Action]
        for action in actionList:
            if action.description[:4] == "Move" and action.subject[0] == "A":
                moveActionList.append(action)
        for action in moveActionList:
            moveActionList.remove(action)
            for action2 in moveActionList:
                self.check_vertex(action, action2)
                self.check_edge(action, action2)
                # For future improvement add here other collisions type

        return self.collisions

    def check_vertex(self, act1: Action, act2: Action):
        if act1.timestep == act2.timestep and act1.end_position == act2.end_position:
            conflict = Collision(act1.timestep, act1.subject, act2.subject, "Vertex")
            # print("\tVertex conflict: " + str(conflict))
            self.collisions.append(conflict)

    def check_edge(self, act1: Action, act2: Action):
        if (
                act1.timestep == act2.timestep and act1.start_position == act2.end_position and act2.start_position == act1.end_position):
            conflict = Collision(act1.timestep, act1.subject, act2.subject, "Edge")
            # print("\tEdge conflict: " + str(conflict))
            self.collisions.append(conflict)

    def evaluate(self):
        self.catch_conflicts()
        self.evaluate_make_span()
        self.evaluate_medium_costs()
        self.evaluate_sum_of_costs()

    @property
    def conflicts(self):
        return self.collisions

    def to_dict(self):
        return {
            "TestName": self.testReference.name,
            "Solved": self.testReference.is_solved,
            "Number of collisions": len(self.collisions),
            "Makespan": self.makeSpan,
            "Sum of Costs": self.sumOfCosts,
            "Medium cost": self.mediumCost,
            "Time elapsed": self.testReference.time_elapsed,
            "Memory usage": self.testReference.memory_usage,
            "Collisions": [collision.to_dict() for collision in self.collisions],
            "TestRun": self.testReference.to_dict()
        }
