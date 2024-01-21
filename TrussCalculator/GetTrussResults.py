# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 09:41:56 2024

@author: someone
"""
from GetAxialForces import *

def GetEdgeStresses(EdgeAxialForces,TrussData):
    EdgeStresses = {}
    for Edge in EdgeAxialForces.keys():
        AxialForce = EdgeAxialForces[Edge]
        Capacity = TrussData["EdgeCapacities"][Edge]
        Stress = AxialForce * Capacity
        EdgeStresses[Edge] = Stress
    return EdgeStresses

def GetEdgeAbsStresses(EdgeStresses):
    for Edge in EdgeAxialForces.keys():
        EdgeStresses[Edge] = abs(EdgeStresses[Edge])
    return EdgeStresses


def GetEdgeMaxStress(EdgeStresses):
    EdgeMaxStress = max(EdgeStresses.values())
    return EdgeMaxStress

def GetEdgeCosts(TrussData):
    EdgeLengths = GetEdgeLengths(TrussData)
    EdgeCosts = {}
    CostFactor = 100
    for Edge in EdgeLengths.keys():
        Length = EdgeLengths[Edge]
        Capacity = TrussData["EdgeCapacities"][Edge]
        Cost = Length * Capacity * CostFactor
        EdgeCosts[Edge] = Cost
    return EdgeCosts

def GetTotalCost(EdgeCosts,TrussData):
    TotalCost = 0
    for Edge, Cost in EdgeCosts.items():
        if TrussData["EdgeInclusions"][Edge]:
            TotalCost += Cost
    return TotalCost

def GetEdgeSxCs(EdgeStresses,EdgeCosts):
    EdgeSxCs = {}
    for Edge, Stress in EdgeStresses.items():
        Cost = EdgeCosts[Edge]
        SxC = Stress * Cost
        EdgeSxCs[Edge] = SxC
    return EdgeSxCs

def GetSumOfSxC(EdgeSxCs,TrussData):
    SumOfSxC = 0
    for Edge, SxC in EdgeSxCs.items():
        if TrussData["EdgeInclusions"][Edge]:
            SumOfSxC += SxC
    return SumOfSxC


def GetTrussResults(TrussData):
    TrussResults = {}
    
    EdgeAxialForces =  GetEdgeAxialForces(TrussData)
    EdgeAbsAxialForces = GetEdgeAbsAxialForces(EdgeAxialForces)
    EdgeStresses = GetEdgeStresses(EdgeAbsAxialForces,TrussData)
    EdgeCosts = GetEdgeCosts(TrussData)
    
    TrussResults["AxialForces"] = EdgeAbsAxialForces
    TrussResults["MaxAxialForce"] = GetEdgeMaxAxialForce(EdgeAbsAxialForces,TrussData)
    TrussResults["Stresses"] = EdgeStresses
    TrussResults["MaxStress"] = GetEdgeMaxStress(EdgeStresses)

    TrussResults["TotalCost"] = GetTotalCost(EdgeCosts,TrussData)
    
    EdgeSxCs = GetEdgeSxCs(EdgeStresses,EdgeCosts)
    TrussResults["SxC"] = EdgeSxCs
    TrussResults["SumOfSxC"] = GetSumOfSxC(EdgeSxCs,TrussData)
    TrussResults["MaxSxC"] = TrussResults["TotalCost"] * TrussResults["MaxStress"]
    return TrussResults


def GetTrussResults_Simplified(TrussData,MinLength=0.17):
    TrussResults = {}
    
    EdgeAxialForces = CheckAndGetEdgeAxialForces(TrussData,MinLength)
    EdgeAbsAxialForces = GetEdgeAbsAxialForces(EdgeAxialForces)
    EdgeStresses = GetEdgeStresses(EdgeAbsAxialForces,TrussData)
    EdgeCosts = GetEdgeCosts(TrussData)
    EdgeSxCs = GetEdgeSxCs(EdgeStresses,EdgeCosts)
    TotalCost = GetTotalCost(EdgeCosts,TrussData)
    
    TrussResults["MaxAxialForce"] = GetEdgeMaxAxialForce(EdgeAbsAxialForces,TrussData)
    TrussResults["MaxStress"] = GetEdgeMaxStress(EdgeStresses)
    TrussResults["SumOfSxC"] = GetSumOfSxC(EdgeSxCs,TrussData)
    TrussResults["MaxSxC"] = TotalCost * TrussResults["MaxStress"]
    return TrussResults
    