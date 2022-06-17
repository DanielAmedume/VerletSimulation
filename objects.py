import numpy

class ball():

  def __init__(self,pos,radius,colour,outlineColour):
    self.pos = numpy.array(pos)
    self.radius = radius
    self.oldPos = pos
    self.acceleration = numpy.array([0,0])
    self.colour = colour
    self.hasHitbox = True
    self.hasGravity = True
    self.canMove = True
    self.doesThings = False
    self.outlineColour = outlineColour
    
  def accelerate(self,acceleration):
    self.acceleration = numpy.add(self.acceleration, acceleration)
  
  def updatePosition(self,dt):
      self.velocity = numpy.array(self.pos-self.oldPos)
      self.oldPos = self.pos

      self.pos = self.pos + self.velocity + self.acceleration * dt * dt
      acceleration = numpy.array([0,0])

class attractor():
  def __init__(self,pos,radius,colour,strength):
    self.pos = numpy.array(pos)
    self.radius = radius
    self.oldPos = pos
    self.acceleration = numpy.array([0,0])
    self.colour = colour
    self.hasHitbox = True
    self.hasGravity = False
    self.canMove = False
    self.doesThings = True
    self.strength = strength
    self.outlineColour = colour

  def do(self,objects):
    for obj in objects:
      if obj.canMove:
        vector = self.pos - obj.pos
        dist = dist = numpy.linalg.norm(vector)
        norm = vector/dist
        obj.accelerate(vector)

