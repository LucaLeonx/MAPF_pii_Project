from result.action import Action
from result.testrun import TestRun
from description.entity_description import EntityDescription
from metrics.agentMetrics import AgentMetrics

class Collision():
    def __init__(self,timestep : int,entity1 : str,entity2 : str):
        self.timestep = timestep
        self.entity1 = entity1
        self.entity2 = entity2

    def __str__(self) -> str:
        return "Collision timestep: " + str(self.timestep) + " | between " + self.entity1 + " and " + self.entity2


class TestMetrics():
    def __init__(self,testRun : TestRun):
        self.testReference = testRun
        self.collitions = [Collision]
        self.agentMetricsList = [AgentMetrics]
        self.actionsWithoutAgent = self.testReference.action_list
        for agent in self.testReference.agents:
            agentMetric = AgentMetrics(agent,self.takeActionsByAgent(agent.name))
            self.agentMetricsList.append(agentMetric)

    def take_actions_by_agent(self,agentName) -> list[Action]:
        return [ action for action in self.actionsWithoutAgent if action.subject == agentName ]

    def evaluate_make_span(self):
        self.makeSpan = max([agentMetrics.timeToReachTarget for agentMetrics in self.agentMetricsList])
        
    def evaluate_sum_of_costs(self):
        self.sumOfCosts = sum([agentMetrics.timeToReachTarget for agentMetrics in self.agentMetricsList])

    def catch_conflicts(self) -> list[Collision]:
        actionList = self.testReference.action_list
        moveActionList = [Action]
        for action in actionList:
            if action.description[:4] == "Move" and action.subject[0] == "A":
                moveActionList.append(action)
        for action in moveActionList:
            moveActionList.remove(action)
            for action2 in moveActionList:
                self.check_vertex(action,action2)
                self.check_edge(action,action2)
                #For future improvement add here other collitions type
                
        return self.collitions
    
    def check_vertex(self,act1 : Action,act2 : Action):
        if (act1.timestep == act2.timestep and act1.end_position == act2.end_position ) :
            conflict = Collision(act1.timestep,act1.subject,act2.subject)
            #print("\tVortex conflict: " + str(conflict))
            self.collitions.append(conflict)
    
    def check_edge(self,act1 : Action,act2 : Action):
        if (act1.timestep == act2.timestep and act1.start_position == act2.end_position and act2.start_position == act1.end_position ) :
            conflict = Collision(act1.timestep,act1.subject,act2.subject)
            #print("\tEdge conflict: " + str(conflict))
            self.collitions.append(conflict)
    