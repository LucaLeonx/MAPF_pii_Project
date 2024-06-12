from typing import List

from description.entity_description import AgentDescription
from result.action import Action


class AgentMetrics:

    def __init__(self, agent: AgentDescription, actions: List[Action]) -> None:
        self._agent = agent
        self._actionList = actions
        self._timeToReachTarget = 0
        self._numOfWait = 0
        self._numOfMove = 0
        self.evaluate()

    def evaluate(self):
        self._timeToReachTarget = len(self._actionList)
        self._numOfWait = len([action for action in self._actionList if action.description == 'Wait'])
        self._numOfMove = len([action for action in self._actionList if action.description == 'Move'])

    @property
    def timeToReachTarget(self):
        return self._timeToReachTarget

    @timeToReachTarget.setter
    def timeToReachTarget(self, value):
        self._timeToReachTarget = value

    @property
    def numberOfWait(self):
        return self._numOfWait

    @numberOfWait.setter
    def numberOfWait(self, value):
        self._numOfWait = value

    @property
    def numberOfMove(self):
        return self._numOfMove

    @numberOfMove.setter
    def numberOfMove(self, value):
        self._numOfMove = value

    def to_dict(self):
        return {
            "agentName": self.agent,
            "timeToReachTarget": self.timeToReachTarget,
            "numberOfWait": self.numberOfWait,
            "numberOfMove": self.numberOfMove,
        }
