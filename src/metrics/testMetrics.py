from result.action import Action
from result.testrun import TestRun
from description.entity_description import EntityDescription
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
        self.timestep = timestep
        self.entity1 = entity1
        self.entity2 = entity2
        self.collType = type

    def to_dict(self):
        return {
            "Collision type": self.collType,
            "timestep": self.timestep,
            "Agent 1": self.entity1,
            "Agent 2": self.entity2
        }

    def __str__(self) -> str:
        return "Collision timestep: " + str(self.timestep) + " | between " + self.entity1 + " and " + self.entity2


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
        self.run()

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

    def run(self):
        self.catch_conflicts()
        self.evaluate_make_span()
        self.evaluate_medium_costs()
        self.evaluate_sum_of_costs()

    def to_dict(self):
        return {
            "TestRun": self.testReference.to_dict(),
            "Collision Detected": [collision.to_dict() for collision in self.collisions],
            "Makespan": self.makeSpan,
            "Sum of Costs": self.sumOfCosts,
            "Medium cost": self.mediumCost,
        }
