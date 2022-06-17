import numpy
import math

class solver():


    def getDist(self,x,y):
       return(math.sqrt(abs(x[0] - y[0])**2 + abs(x[1] - y[1])**2))
    
    def __init__(self, gravity,x,y):
        self.G = gravity
        self.width = x
        self.height = y
        self.center = (x/2,y/2)
        self.radius = 0.4*y

    def updateG(self):
        if self.G == [0,0]:
            self.G = [0,1000]
        else:
            self.G = [0,0]

    def applyGravity(self, objects): 
    
        for obj in objects:
            if obj.hasGravity:
                obj.accelerate(self.G)

    def getGravity(self):
        return(self.G)
            
    def updatePositions(self, objects, dt):
        for obj in objects:
            if obj.canMove:
                obj.updatePosition(dt)

    def constrain(self,objects):

        for obj in objects:
            to_obj = obj.pos - self.center
            dist = self.getDist(obj.pos, self.center)
            if dist > (self.radius - obj.radius):
                normDist = numpy.divide(to_obj,dist)
                obj.pos = self.center + (normDist * (self.radius - obj.radius))


    def solveCollisions(self,objects):
        for current in objects:
            for collider in objects:
                
                if current == collider:
                    break

                if not(collider.hasHitbox and current.hasHitbox):
                    break

                collisionVector = current.pos - collider.pos
                dist = self.getDist(current.pos, collider.pos)


                if dist < current.radius + collider.radius:
                    norm = collisionVector / dist
                    delta = (current.radius + collider.radius) - dist
                    change = 0.5 * delta * norm
                    current.pos = numpy.add(current.pos,change * current.canMove,casting='unsafe')
                    collider.pos = numpy.subtract(collider.pos,change*collider.canMove,casting='unsafe')    


    def objectFunctions(self, objects):
        for obj in objects:
            if obj.doesThings:
                obj.do(objects)
        
    def getRadius(self):
        return(self.radius)

    def getCenter(self):
        return(list(self.center))
 
    def solve(self, objects, dt,substeps):


        subDT = dt /substeps**2

        for i in range(substeps):
            
            self.applyGravity(objects)

            self.objectFunctions(objects)

            self.constrain(objects)

            self.solveCollisions(objects)

            self.updatePositions(objects,subDT)
