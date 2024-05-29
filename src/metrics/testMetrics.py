from result.action import Action

class TestMetrics():
    def __init__(self,testRun):
        self.testReference = testRun

    def divideInGroups(self,actionList) -> list[list[Action]]:        
        listsByTimestep = [[]]
        for action in actionList:
            print(action)   
            if action.timestep > len(listsByTimestep):
                listsByTimestep.insert(action.timestep,[action])
            else: 
                listsByTimestep[action.timestep()].append(action)
        return listsByTimestep

    def findCollision(self) -> list[tuple[Action,Action]]:
        groupsByTimestep = self.divideInGroups(self.testReference.action_list)
        collisionList = []
        for actionGroup in groupsByTimestep:
            collisionList.extend(self.checkVortexCollisions(actionGroup))
            collisionList.extend(self.checkEdgeCollisions(actionGroup))
            
        return collisionList


    def checkVortexCollisions(self,actionList) -> list[tuple[Action,Action]] :
        collisions = [tuple[Action,Action]]
        for action in actionList:
            if actionList.count(action.end_position) > 1:
                #conflict = actionList.
                collisions.append(tuple[action,actionList])    
        

    def checkEdgeCollisions(self,actionList) -> list[tuple[Action,Action]] :
        collision = [tuple[Action]]


    def bruteForce(self) -> list:
        actionList = self.testReference.action_list
        moveActionList = []
        for action in actionList:
            if action.description[:4] == "Move" and action.subject[0] == "A":
                print(action)
                moveActionList.append(action)
        collitions = [Collision]
        print("Collisions : ")
        for action in moveActionList:
            moveActionList.remove(action)
            for action2 in moveActionList:
                #Edge conflict
                if (action.timestep == action2.timestep and action.start_position == action2.end_position and action2.start_position == action.end_position ) :
                    conflict = Collision(action.timestep,action.subject,action2.subject)
                    print("\tEdge conflict: " + str(conflict))
                    collitions.append(conflict)
                    continue
                #Vertex conflict
                if (action.timestep == action2.timestep and action.end_position == action2.end_position ) :
                    conflict = Collision(action.timestep,action.subject,action2.subject)
                    print("\tVortex conflict: " + str(conflict))
                    collitions.append(conflict)
    
        return collitions
    
class Collision():
    def __init__(self,timestep,entity1,entity2):
        self.timestep = timestep
        self.entity1 = entity1
        self.entity2 = entity2

    def __str__(self) -> str:
        return "Collision timestep: " + str(self.timestep) + " | between " + self.entity1 + " and " + self.entity2