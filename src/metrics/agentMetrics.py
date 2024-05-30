from description.entity_description import AgentDescription,EntityDescription
from result.action import Action

class AgentMetrics():
    
    def __init__(self,agent : AgentDescription, actions : list[Action]) -> None:
        self.agent = agent
        self.actionList = actions
        self.evaluate()

    def evaluate(self):
        self.timeToReachTarget = self.actionList.__len__        
        self.numOfWait = [action for action in self.actionList if action.description == 'Wait'].__len__
        self.numOfMove = [action for action in self.actionList if action.description == 'Move'].__len__

    @property
    def timeToReachTarget(self):
        return self.timeToReachTarget
    
    @property
    def numberOfWait(self):
        return self.numOfWait
    
    @property
    def numberOfMove(self):
        return self.numOfMove
    
    def to_dict(self):
        return  {
            "agentName" : self.agent,
            "timeToReachTarget" : self.timeToReachTarget,
            "numberOfWait" : self.numberOfWait,
            "numberOfMove" : self.numberOfMove,
        }