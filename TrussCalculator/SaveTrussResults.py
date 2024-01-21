# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 14:36:54 2024

@author: someone
"""
from IterateNodes import *

def GetMinimumResultIDs(IteratedResults):
    MinimumResultIDs = {}
    MinimumResultValues = {}
    for ResultType, value in IteratedResults[1].items():
        MinimumResultIDs[ResultType] = 1
        MinimumResultValues[ResultType] = value
    for ResultID, TrussResults in IteratedResults.items():
        for ResultType, value in TrussResults.items():
            if value < MinimumResultValues[ResultType]:
                MinimumResultIDs[ResultType] = ResultID
                MinimumResultValues[ResultType] = value
                
    return MinimumResultIDs

def GetFilteredResultIDs(IteratedResults,MinimumResultIDs):
    FilteredResultIDs = {}
    for ResultType, ResultID in MinimumResultIDs.items():
        FilteredResultIDs[ResultID] = IteratedResults[ResultID]
    return FilteredResultIDs
    
def GetMinimumResultValues(IteratedResults,MinimumResultIDs):
    MinimumResultValues = {}
    for ResultType, ResultID in MinimumResultIDs.items():
        MinimumResultValues[ResultType] = IteratedResults[ResultID][ResultType]
    return MinimumResultValues

#-------------------------------------------------Save Truss Results-----------------------------------------------

def SaveIteratedResults(TrussData,TweakData):
    IteratedResults = GetIteratedResults(TrussData,TweakData)
    
    file = open("TrussResults\\IteratedResults.csv","w")
    Layers = len(TweakData)
    
    row_title = ["ResultID"] # Write Row Title
    for n in range(Layers):
        Node = TweakData[n][0]
        row_title.append("Node" + str(Node)+"_x")
        row_title.append("Node" + str(Node)+"_y")
    for ResultType in IteratedResults[1].keys():
        row_title.append(ResultType)
    file.writelines(",".join(row_title) + "\n")
    
    IteratedNodes = GetIteratedNodes(TweakData) # Write Row content
    for ResultID, NodeCoords in IteratedNodes.items():
        row = [str(ResultID)]
        for n in range(Layers):
            Node = TweakData[n][0]
            Coord = IteratedNodes[ResultID][Node]
            x = Coord[0]
            y = Coord[1]
            row.append(str(x))
            row.append(str(y))
        for value in IteratedResults[ResultID].values():
            row.append(str(value))

        file.writelines(",".join(row) + "\n")
    file.close()

def SaveIteratedResultAnalysis(TrussData,TweakData):
    IteratedResults = GetIteratedResults(TrussData,TweakData)
    
    file = open("TrussResults\\IteratedResultAnalysis.txt","w")
    file.writelines("----Result Analysis----\n")
    Layers = len(TweakData)
    
    MinimumResultIDs = GetMinimumResultIDs(IteratedResults)
    FilteredResultIDs = GetFilteredResultIDs(IteratedResults, MinimumResultIDs)
    MinimumResultValues = GetMinimumResultValues(IteratedResults, MinimumResultIDs)
    
    for ResultType, ResultID in MinimumResultIDs.items():
        value = MinimumResultValues[ResultType]
        value = "%.4f" % value
        
        line = "Minimum " + ResultType + ": " + value + " (ResultID = " + str(ResultID) + ")"
        file.writelines(line + "\n")
    
    file.writelines("\n----Filtered ResultIDs----\n")
    row_title = ["ResultID"]
    for n in range(Layers):
        Node = TweakData[n][0]
        row_title.append("Node" + str(Node)+"_x")
        row_title.append("Node" + str(Node)+"_y")
    for ResultType in IteratedResults[1].keys():
        row_title.append(ResultType)
    file.writelines(",".join(row_title) + "\n")
    
    IteratedNodes = GetIteratedNodes(TweakData)
    for ResultID in FilteredResultIDs.keys():
        NodeCoords = IteratedNodes[ResultID]
        row = [str(ResultID)]
        for n in range(Layers):
            Node = TweakData[n][0]
            Coord = IteratedNodes[ResultID][Node]
            x = Coord[0]
            y = Coord[1]
            row.append(str(x))
            row.append(str(y))
        for value in IteratedResults[ResultID].values():
            row.append(str(value))

        file.writelines(",".join(row) + "\n")
    file.close()