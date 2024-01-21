# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 13:03:11 2024

@author: someone
"""

from ImportSampleTruss import *
from SaveTrussResults import *
from ViewTruss import *

filename = "cantilever"
TrussData = ImportSampleTruss(filename)

TrussData = GetTweakedTrussData(TrussData, "4", (0.845,-0.751))
ViewTrussResults(TrussData,"AxialForces")