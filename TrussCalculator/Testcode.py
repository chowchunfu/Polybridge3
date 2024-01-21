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

TweakData = [("4",XCoords1,YCoords1),("2",XCoords2,YCoords2)]

allnodes = GetIteratedNodes(TweakData)

SaveIteratedResultAnalysis(TrussData, TweakData)
