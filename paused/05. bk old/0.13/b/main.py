#!/usr/bin/python
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 13-b :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
from land import Zululand
from zulus import Zulu
from rules import Slide
from shapes import Rect
#
#--- FUNCTIONS ----------------------------------------------------------------
def populate():
    # define zulus
    z1 = Zulu()
    z1.shape=Rect(100,100)
    z1.centroid=[0,0,0]
    z1.color=[123,3,212]
    # Define as many rules as necessary, append zulus to rules
    r1=Slide(27,0)
    r1.apply_to(z1)
    r2=Bounce(land.boundaries)
    r2.apply_to(z1)

#
##  MAIN ----------------------------------------------------------------------
def main():
    zl13=Zululand()
    populate()
    zl13.run()
##  ---------------------------------------------------------------------------
if __name__ == "__main__": main()
