# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 12:48:13 2024

@author: someone
"""

from ImportSampleTruss import *
from SaveTrussResults import *
from ViewTruss import *

filename = "cantilever"
TrussData = ImportSampleTruss(filename)

XCoords1 = GetCoordsToIterate(0.75,0.02,10)
YCoords1 = GetCoordsToIterate(-0.75,0.02,10)

XCoords2 = GetCoordsToIterate(0.125,0,10)
YCoords2 = GetCoordsToIterate(-0.99,0.02,10)

TweakData = [("4",XCoords1,YCoords1),("3",XCoords2,YCoords2)]

TrussData = GetTweakedTrussData(TrussData, "4", (0.84,-0.84))
TrussData = GetTweakedTrussData(TrussData, "2", (0.125,-1.08))

ViewTrussResults(TrussData, "AxialForces")