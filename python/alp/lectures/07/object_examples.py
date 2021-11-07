class Osoba:
  pass

o=Osoba()
o.jmeno="Karel"
o.prijmeni="Novák"

print(o.jmeno+" "+o.prijmeni)

######################################################################

class Osoba:
  def print(self):
    print(self.jmeno+" "+self.prijmeni)
    
o=Osoba()
o.jmeno="Karel"
o.prijmeni="Novák"

o.print()

######################################################################

class Osoba:
  def __init__(self,jmeno,prijmeni):
    self.jmeno=jmeno
    self.prijmeni=prijmeni

  def print(self):
    print(o.jmeno+" "+o.prijmeni)

o=Osoba("Karel","Novák")
o.print()    

######################################################################
import math

class Point:
  """ 2D point with attributes 'x' and 'y' """
  def __init__(self,x,y):
    self.x=x
    self.y=y

def distance(r,s):
  """ Vypočítá vzdálenost dvou bodů 'r','s' typu Point """
  return math.sqrt((r.x-s.x)**2+(r.y-s.y)**2)

r=Point(10,20)
s=Point(13,24)
print(distance(r,s))
