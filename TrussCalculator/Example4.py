# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 09:58:03 2024

@author: someone
"""

from ImportSampleTruss import *
from SaveTrussResults import *
from ViewTruss import *

filename = "cantilever2_Ex"
TrussData = ImportSampleTruss(filename)

XCoords1 = GetCoordsToIterate(0.125,0,100)
YCoords1 = GetCoordsToIterate(-1,0.002,1000)

TweakData = [("2",XCoords1,YCoords1)]

SaveIteratedResults(TrussData,TweakData)