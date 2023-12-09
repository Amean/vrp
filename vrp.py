import sys
import math
import io

#function for calculating distance
#takes 
#load data from .txt
#start new driver, keep routing to next job until distance is equal to half 12*60, then return home\

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def toString(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

def distanceBetweenPoints(p1, p2):
    xDiff = p1.x - p2.x
    yDiff = p1.y - p2.y
    return math.sqrt(xDiff*xDiff + yDiff*yDiff)
    
class Load:
    def __init__(self, id, pickup, dropoff):
        self.id = id
        self.pickup = pickup
        self.dropoff = dropoff
        
class VRP:
    def __init__(self, loads):
        self.loads = loads
    def toProblemString(self):
        s = "loadNumber pickup dropoff\n"
        for idx, load in enumerate(self.loads):
            s += str(idx+1) + " " + load.pickup.toString() + " " + load.dropoff.toString() + "\n"
        return s
    def solver(self):
        driverRoute = []
        driverCoordinates = Point(0,0)
        driverDistance= 0
        for load in self.loads:
            loadDistance = distanceBetweenPoints(driverCoordinates, load.pickup) + distanceBetweenPoints(load.pickup, load.dropoff)
            
            #print(driverRoute)
            #print(load.id)
            #print(driverDistance)
            #print(driverDistance + loadDistance + distanceBetweenPoints(load.dropoff, Point(0,0)))
            if driverDistance + loadDistance + distanceBetweenPoints(load.dropoff, Point(0,0)) > 720.0:
                #print("reset")
                print(driverRoute)
                driverRoute = []
                driverCoordinates = Point(0,0)
                driverDistance = 0
            driverRoute.append(int(load.id))
            driverDistance += distanceBetweenPoints(driverCoordinates, load.pickup) + distanceBetweenPoints(load.pickup, load.dropoff)
            driverCoordinates = load.dropoff
        print(driverRoute)



def loadProblemFromFile(filePath):
    f = open(filePath, "r")
    problemStr = f.read()
    f.close()
    return loadProblemFromProblemStr(problemStr)

def getPointFromPointStr(pointStr):
    pointStr = pointStr.replace("(","").replace(")","")
    splits = pointStr.split(",")
    return Point(float(splits[0]), float(splits[1]))

def loadProblemFromProblemStr(problemStr):
    loads = []
    buf = io.StringIO(problemStr)
    gotHeader = False
    while True:
        line = buf.readline()
        if not gotHeader:
            gotHeader = True
            continue
        if len(line) == 0:
            break
        line = line.replace("\n", "")
        splits = line.split()
        id = splits[0]
        pickup = getPointFromPointStr(splits[1])
        dropoff = getPointFromPointStr(splits[2])
        loads.append(Load(id, pickup, dropoff))
    return VRP(loads)


if __name__ == "__main__":
    #print(sys.argv[1])
    problem = loadProblemFromFile(sys.argv[1])
    #print(problem.toProblemString())
    problem.solver()
    