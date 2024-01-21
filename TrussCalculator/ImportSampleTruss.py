# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 21:18:18 2024

@author: someone
"""

def ImportSampleTruss(filename):
    file = open("SampleTruss\\" + filename + ".txt","r")
    
    TrussData = {}
   
    TrussData["NodeCoords"] = ReadTrussData(file,2,"Float")
    TrussData["NodeRestraints"] = ReadTrussData(file,2,"Int")
    TrussData["NodeLoads"] = ReadTrussData(file,2,"Float")
    TrussData["EdgeConnections"] = ReadTrussData(file,2,"Str")
    TrussData["EdgeCapacities"] = ReadTrussData(file,1,"Float")
    TrussData["EdgeInclusions"] = ReadTrussData(file,1,"Int")
    
    return TrussData

def ReadTrussData(file, amount, valuetype): #For Single Datum
    line = file.readline()
    Data = {}
    while line != "\n" and line != "":
        line = file.readline()
        if line != "\n" and line != "":
            linelength = line.index("\n")
            linelist = line[0:linelength].split(":")
            key = linelist[0]
            
            if amount == 1 and valuetype == "Int":
                value = int(linelist[1])
            elif amount == 1 and valuetype == "Float":
                value = float(linelist[1])
                
            elif amount == 2 and valuetype == "Str":
                value = linelist[1].split()
            elif amount == 2 and valuetype == "Int":
                value = linelist[1].split()
                value[0] = int(value[0])
                value[1] = int(value[1])
            elif amount == 2 and valuetype == "Float":
                value = linelist[1].split()
                value[0] = float(value[0])
                value[1] = float(value[1])
                
            Data[key] = value
    return Data


def SaveSampleTruss(TrussData, filename):
    file = open("SavedTruss\\" + filename + ".txt","w")
    file.writelines("Node:Coord_x Coord_y\n")
    for Node in NodeCoords.keys():
        Coord = TrussData["NodeCoords"][Node]
        file.writelines(Node + ":" + str(Coord[0]) + " " + str(Coord[1]) + "\n")
    file.writelines("\nNode:NodeRestraint_x NodeRestraint_y\n")
    for Node in NodeRestraints.keys():
        Restraint = TrussData["Restraints"][Node]
        file.writelines(Node + ":" + str(Restraint[0]) + " " + str(Restraint[1]) + "\n")
    file.writelines("\nNode:Load_x Load_y\n")
    for Node in NodeLoads.keys():
        Load = TrussData["NodeLoads"][Node]
        file.writelines(Node + ":" + str(Load[0]) + " " + str(Load[1]) + "\n")
    file.writelines("\nEdge:Connection1 Connection2\n")
    for Edge in TrussData["EdgeConnections"].keys():
        Connection = EdgeConnections[Edge]
        file.writelines(Edge + ":" + str(Connection[0]) + " " + str(Connection[1]) + "\n")
    file.writelines("\nEdge:Capacity\n")
    for Edge in EdgeCapacities.keys():
        Capacity = EdgeCapacities[Edge]
        file.writelines(Edge + ":" + str(Capacity) + "\n")
    file.writelines("\nEdge:EdgeInclusions\n")
    for Edge in EdgeInclusions.keys():
        Inclusion = EdgeInclusions[Edge]
        file.writelines(Edge + ":" + str(Inclusion) + "\n")
    
    file.close()
    return 