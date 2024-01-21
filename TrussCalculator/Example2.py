# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 10:19:22 2024

@author: someone
"""

from ImportSampleTruss import *
from SaveTrussResults import *
from ViewTruss import *

filename = "cantilever"
TrussData = ImportSampleTruss(filename)

XCoords1 = GetCoordsToIterate(0.75,0.02,10)
YCoords1 = GetCoordsToIterate(-0.75,0.02,10)

TweakData = [("4",XCoords1,YCoords1)]

SaveIteratedResultAnalysis(TrussData,TweakData)