from result.action import Action

class TestMetrics():
    def __init__(self,testRun):
        self.testReference = testRun

    def divideInGroups(self,actionList) -> list[list[Action]]:        
        listsByTimestep = [[]]
        for action in actionList:
            print(action)   
            if action.timestep() > len(listsByTimestep):
                listsByTimestep.insert(action.timestep(),[action])
            else: 
                listsByTimestep[action.timestep()].append(action)
        return listsByTimestep

    def findCollision(self) -> list[tuple[Action,Action]]:
        groupsByTimestep = self.divideInGroups(self.testReference.action_list())
        collisionList = []
        for actionGroup in groupsByTimestep:
            collisionList.extend(self.checkVortexCollisions(actionGroup))
            collisionList.extend(self.checkEdgeCollisions(actionGroup))
            
        return collisionList


    def checkVortexCollisions(self,actionList) -> list[tuple[Action,Action]] :
        collisions = [tuple[Action,Action]]
        for action in actionList:
            if actionList.count(action.end_position()) > 1:
                #conflict = actionList.
                collisions.append(tuple[action,actionList])    
        

    def checkEdgeCollisions(self,actionList) -> list[tuple[Action,Action]] :
        collision = [tuple[Action]]


    def bruteForce(self) -> list[tuple[Action,Action]]:
        actionList = self.testReference.action_list()
        collitions = [tuple[Action,Action]]
        for action in actionList:
            for action2 in actionList.remove(action):
                #Edge conflict
                if (action.timestep() == action2.timestep() and action.start_position() == action2.end_position() and action2.start_position() == action.end_position() ) :
                    print(tuple[action,action2])
                    collitions.append(tuple[action,action2])
                    continue
                #Vertex conflict
                if (action.timestep() == action2.timestep() and action.end_position() == action2.end_position() ) :
                    print(tuple[action,action2])
                    collitions.append(tuple[action,action2])
        
        return collitions