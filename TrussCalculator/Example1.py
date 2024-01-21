# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 09:58:03 2024

@author: someone
"""

from ImportSampleTruss import *
from SaveTrussResults import *
from ViewTruss import *

filename = "cantilever2"
TrussData = ImportSampleTruss(filename)

ViewTruss(TrussData)