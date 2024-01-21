# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 20:23:07 2024

@author: someone
"""
import numpy as np

def CheckMinEdgeLengths(TrussData, MinLength):
    EdgeLengths = GetEdgeLengths(TrussData)
    check = True
    
    for length in EdgeLengths.values():
        if length < MinLength:
            check = False
    return check
    

def GetEdgeLengths(TrussData):
    EdgeLengths = {}
    for Edge in TrussData["EdgeConnections"].keys():
        Node1 = TrussData["EdgeConnections"][Edge][0]
        Node2 = TrussData["EdgeConnections"][Edge][1]
        NodeCoord1 = TrussData["NodeCoords"][Node1]
        NodeCoord2 = TrussData["NodeCoords"][Node2]
        
        dx = NodeCoord1[0] - NodeCoord2[0]
        dy = NodeCoord1[1] - NodeCoord2[1]
        length = (dx**2+dy**2)**0.5
        EdgeLengths[Edge] = length
        
    return EdgeLengths
    
def GetEdgeAlphas(TrussData):
    EdgeAlphas = {}
    for Edge in TrussData["EdgeConnections"].keys():
        Node1 = TrussData["EdgeConnections"][Edge][0]
        Node2 = TrussData["EdgeConnections"][Edge][1]
        NodeCoord1 = TrussData["NodeCoords"][Node1]
        NodeCoord2 = TrussData["NodeCoords"][Node2]
        
        dx = NodeCoord2[0] - NodeCoord1[0]
        dy = NodeCoord2[1] - NodeCoord1[1]
        if dx == 0:
            if dy >= 0: #Vertical line
                Alpha = 90 / 180 * np.pi
            else:
                Alpha = 270 / 180 * np.pi
        elif dx >0: #Quadrant 1, 4
            Alpha = np.arctan(dy/dx)
        else: #Quadrant 2, 3
            Alpha = np.pi + np.arctan(dy/dx)
        EdgeAlphas[Edge] = Alpha
    return EdgeAlphas

def GetEdgeAxialForces(TrussData):
    EdgeAxialForces = {}
    EdgeLengths = GetEdgeLengths(TrussData)
    EdgeAlphas = GetEdgeAlphas(TrussData)

    EdgeLocalMatrices = {}
    EdgeTransferMatrices = {}
    Edge_list = TrussData["EdgeConnections"].keys()
    Node_list = TrussData["NodeCoords"].keys()

    for Edge in Edge_list: #Get length, alpha of a member
        Length = EdgeLengths[Edge]
        Alpha = EdgeAlphas[Edge]
        
        LocalMatrix = np.zeros((4,4))
        TransferMatrix = np.zeros((4,4))
        
        sine = np.sin(Alpha)
        cosine = np.cos(Alpha)
        
        A = [[cosine**2, sine * cosine], [sine * cosine, sine**2]]
        T = [[cosine, sine], [-sine, cosine]]

        for xbig in range(0,4,2):
            for ybig in range(0,4,2):
                for xsmall in range(0,2):
                    for ysmall in range(0,2):
                        if xbig + ybig == 2:
                            LocalMatrix[xbig+xsmall][ybig+ysmall] = A[0+xsmall][0+ysmall] * -1
                        else:
                            LocalMatrix[xbig+xsmall][ybig+ysmall] = A[0+xsmall][0+ysmall]
                            TransferMatrix[xbig+xsmall][ybig+ysmall] = T[0+xsmall][0+ysmall]
            
        EdgeLocalMatrices[Edge] = LocalMatrix / Length
        EdgeTransferMatrices[Edge] = TransferMatrix
        
    size = 2 * len(Node_list)
    GlobalMatrix = np.zeros((size,size))
    RestraintMatrix = []
    LoadMatrix = []
    PositionMatrix = list(range(size))

      
    for Edge in Edge_list:
        LocalMatrix = EdgeLocalMatrices[Edge]
        Connection1 = TrussData["EdgeConnections"][Edge][0]
        Connection2 = TrussData["EdgeConnections"][Edge][1]
        
        columns = [int(Connection1)*2-2,int(Connection1)*2-1,int(Connection2)*2-2,int(Connection2)*2-1]
        rows = columns
        
        for j in range(0,4):
            for i in range(0,4):
                column = columns[j]
                row = rows[i]
                GlobalMatrix[row][column] += LocalMatrix[i][j]
        
    for Node in Node_list:
        RestraintMatrix.append(TrussData["NodeRestraints"][Node][0])
        RestraintMatrix.append(TrussData["NodeRestraints"][Node][1])
        LoadMatrix.append(TrussData["NodeLoads"][Node][0])
        LoadMatrix.append(TrussData["NodeLoads"][Node][1])

    for i in range(size-1,-1,-1):
        if RestraintMatrix[i] == 0:
            GlobalMatrix = np.delete(GlobalMatrix,i,0)
            GlobalMatrix = np.delete(GlobalMatrix,i,1)
            LoadMatrix = np.delete(LoadMatrix,i,0)
            PositionMatrix = np.delete(PositionMatrix,i,0)
            
    determinant = np.linalg.det(GlobalMatrix)

    if determinant > 0.001:
        result = np.linalg.solve(GlobalMatrix,LoadMatrix) #Get Delta
        GlobalDeltaMatrix = np.zeros((size,1))
        
        for i in range(len(PositionMatrix)):
            pos = PositionMatrix[i]
            GlobalDeltaMatrix[pos] = result[i]
        
        
        for Edge in Edge_list:
            LocalMatrix = EdgeLocalMatrices[Edge]
            TransferMatrix = EdgeTransferMatrices[Edge]
            
            Connection1 = TrussData["EdgeConnections"][Edge][0]
            Connection2 = TrussData["EdgeConnections"][Edge][1]
            columns = [int(Connection1)*2-2,int(Connection1)*2-1,int(Connection2)*2-2,int(Connection2)*2-1]
            
            LocalDeltaMatrix = np.zeros((4,1))
            for i in range(4):
                pos = columns[i]
                LocalDeltaMatrix[i] = GlobalDeltaMatrix[pos]
        
            AxialForceMatrix = np.dot(LocalMatrix, LocalDeltaMatrix)
            AxialForceMatrix_Transfer = np.dot(TransferMatrix,AxialForceMatrix)
            AxialForce = float(AxialForceMatrix_Transfer[0] + AxialForceMatrix_Transfer[1])
            
            EdgeAxialForces[Edge] = AxialForce
        
    else:
        for Edge in Edge_list:
            EdgeAxialForces[Edge] = 10000
    
    return EdgeAxialForces

def CheckAndGetEdgeAxialForces(TrussData,MinLength=0.17):
    if CheckMinEdgeLengths(TrussData, MinLength):
        EdgeAxialForces = GetEdgeAxialForces(TrussData)
    else:
        EdgeAxialForces = {}
        for Edge in TrussData["EdgeConnections"].keys():
            EdgeAxialForces[Edge] = 10000
    return EdgeAxialForces


def GetEdgeAbsAxialForces(EdgeAxialForces):
    for Edge in EdgeAxialForces.keys():
        EdgeAxialForces[Edge] = abs(EdgeAxialForces[Edge])
    return EdgeAxialForces
    
def GetEdgeMaxAxialForce(EdgeAxialForces,TrussData):
    EdgeMaxAxialForce = 0
    
    for Edge, AxialForce in EdgeAxialForces.items():
        if AxialForce > EdgeMaxAxialForce and TrussData["EdgeInclusions"][Edge]:
            EdgeMaxAxialForce = AxialForce
    return EdgeMaxAxialForce
    
