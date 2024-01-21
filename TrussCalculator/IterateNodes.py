# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 11:45:44 2024

@author: someone
"""
from GetTrussResults import *

def GetCoordsToIterate(Center,step,nodes):
    
    if step == 0:
        Coords = [Center]
    else:
        CoordRange = step * (nodes - 1)
        Start = Center - CoordRange / 2
        Coords = []
        for i in range(nodes):
            coord = Start + step * i
            coord = round(coord,4)
            Coords.append(coord)
    return Coords


def GetTweakedTrussData(TrussData,Node,Coord):
    TrussData["NodeCoords"][Node][0] = Coord[0]
    TrussData["NodeCoords"][Node][1] = Coord[1]
    return TrussData


def GetRecursivelyTweakedNodes(n,Layers,TweakData,RecursivelyTweakedNodes,TweakedNodes):
        if n == Layers:
            RecursivelyTweakedNodes += TweakedNodes
        else:
            Xrange = TweakData[n][1]
            Yrange = TweakData[n][2]
            for x in Xrange:
                for y in Yrange:
                    TweakedNodes[n] = (x,y)
                    GetRecursivelyTweakedNodes(n+1,Layers,TweakData,RecursivelyTweakedNodes,TweakedNodes)

def GetIteratedNodes(TweakData):
    Layers = len(TweakData)
    TweakedNodes = []
    for i in range(Layers):
        TweakedNodes.append((0,0))
    
    RecursivelyTweakedNodes = []
    GetRecursivelyTweakedNodes(0,Layers,TweakData,RecursivelyTweakedNodes,TweakedNodes) 
    NumberOfData = int(len(RecursivelyTweakedNodes) / Layers)
    
    IteratedNodes = {} #Tidy Data
    for DataID in range(1,NumberOfData+1):
        IteratedNodes[DataID] = {}
        for n in range(Layers):
            Node = TweakData[n][0]
            Coord = RecursivelyTweakedNodes[Layers*DataID-Layers+n]
            IteratedNodes[DataID][Node] = Coord
    
    return IteratedNodes


def GetIteratedResults(TrussData,TweakData):
    IteratedNodes = GetIteratedNodes(TweakData)
    
    IteratedResults = {}
    for ResultID, NodeData in IteratedNodes.items():
        NodeData = IteratedNodes[ResultID]
        for Node, Coord in NodeData.items():
            TrussData = GetTweakedTrussData(TrussData,Node,Coord)
        TrussResults = GetTrussResults_Simplified(TrussData)
        print(ResultID,TrussResults)
        IteratedResults[ResultID] = TrussResults

    return IteratedResults


