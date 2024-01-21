# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 11:47:39 2024

@author: someone
"""

import tkinter as tk
from PIL import ImageTk, Image
from GetTrussResults import *

def GetTrussNWCoord(TrussData):
    x_min = TrussData["NodeCoords"]["1"][0]
    y_max = TrussData["NodeCoords"]["1"][1]
    for Coord in TrussData["NodeCoords"].values():
        if Coord[0] < x_min:
            x_min = Coord[0]
        if Coord[1] > y_max:
            y_max = Coord[1]
    return x_min,y_max

def GetEdgeLabelCoord(TrussData,Edge,MaxOffset):
  
    Connection = TrussData["EdgeConnections"][Edge]
    Node1 = Connection[0]
    Node2 = Connection[1]
    Coord1 = TrussData["NodeCoords"][Node1]
    Coord2 = TrussData["NodeCoords"][Node2]
    
    dx = Coord2[0] - Coord1[0]
    dy = Coord2[1] - Coord1[1]
    
    x_center = (Coord1[0] + Coord2[0]) * 0.5
    y_center = (Coord1[1] + Coord2[1]) * 0.5
    
    if dx == 0: #Vertical line
        x_offset = -MaxOffset
        y_offset = 0
    elif dx > 0:
        angle = np.arctan(dy/dx)
        offset_angle = angle + np.pi/2
        x_offset = MaxOffset * np.sin(angle)
        y_offset = MaxOffset * np.cos(angle)
        
    elif dx < 0:
        angle = np.pi + np.arctan(dy/dx)
        offset_angle = angle + np.pi/2
        x_offset = MaxOffset * np.sin(angle)
        y_offset = MaxOffset * np.cos(angle)
        
    EdgeXCoord = x_center + x_offset
    EdgeYCoord = y_center - y_offset
    
    return EdgeXCoord,EdgeYCoord

def GetWindowSize(TrussData):
    x_min = TrussData["NodeCoords"]["1"][0]
    x_max = TrussData["NodeCoords"]["1"][0]
    y_min = TrussData["NodeCoords"]["1"][1]
    y_max = TrussData["NodeCoords"]["1"][1]
    for Coord in TrussData["NodeCoords"].values():
        if Coord[0] < x_min:
            x_min = Coord[0]
        elif Coord[0] > x_max:
            x_max = Coord[0]
        if Coord[1] < y_min:
            y_min = Coord[1]   
        elif Coord[1] > y_max:
            y_max = Coord[1]
            
    x_span = x_max - x_min
    y_span = y_max - y_min
    
    WindowLength = int(200 + x_span*200)
    WindowWidth = int(200 + y_span*200)
    WindowSize = str(WindowLength) + "x" + str(WindowWidth)
    return WindowSize

def GetCanvasCoord(Coord,TrussNWCoord):
    x_relative = Coord[0] - TrussNWCoord[0]
    y_relative = Coord[1] - TrussNWCoord[1]
    CanvasX = int(100 + 200*x_relative)
    CanvasY = int(100 - 200*y_relative)
    CanvasCoord = (CanvasX,CanvasY)
    return CanvasCoord

#-------------------------------------------------View Truss-----------------------------------------------
def DrawCanvasEdge(TrussData):
    TrussNWCoord = GetTrussNWCoord(TrussData)
    for Connection in TrussData["EdgeConnections"].values():
        Node1 = Connection[0]
        Node2 = Connection[1]
        
        Coord1 = TrussData["NodeCoords"][Node1]
        Coord2 = TrussData["NodeCoords"][Node2]
        
        CanvasCoord1 = GetCanvasCoord(Coord1,TrussNWCoord)
        CanvasCoord2 = GetCanvasCoord(Coord2,TrussNWCoord)
        
        x1 = CanvasCoord1[0]
        y1 = CanvasCoord1[1]
        x2 = CanvasCoord2[0]
        y2 = CanvasCoord2[1]
    
        canvas.create_line(x1,y1,x2,y2,width=4)

def DrawCanvasNode(TrussData):
    global ImageNodes
    TrussNWCoord = GetTrussNWCoord(TrussData)
    ImageNodes = {}
    for Node, Coord in TrussData["NodeCoords"].items():
        Restraint = TrussData["NodeRestraints"][Node]
        if Restraint == [0,0]:
            ImageName = "Anchor"
        else:
            ImageName = "Node"
        
        CanvasCoord = GetCanvasCoord(Coord,TrussNWCoord)
        CanvasX = CanvasCoord[0]
        CanvasY = CanvasCoord[1]
        
        ImageNode = Image.open("images\\" + ImageName +".png")
        ImageNodes[Node] = ImageTk.PhotoImage(ImageNode)
        canvas.create_image(CanvasX,CanvasY,anchor="center",image=ImageNodes[Node])
        

def LabelNodeCoords(TrussData):
    TrussNWCoord = GetTrussNWCoord(TrussData)
    for Node, Coord in TrussData["NodeCoords"].items():
        CanvasCoord = GetCanvasCoord(Coord,TrussNWCoord)
        CanvasX = CanvasCoord[0]
        CanvasY = CanvasCoord[1]
        
        NodeText = "Node" + Node + "\n" + str(tuple(Coord))
        canvas.create_text(CanvasX,CanvasY-25, text=NodeText,fill="#808000")
        
def LabelEdgeIDs(TrussData,DataType):
    TrussNWCoord = GetTrussNWCoord(TrussData)
    for Edge in TrussData["EdgeConnections"].keys():
        EdgeCoord = GetEdgeLabelCoord(TrussData, Edge,0.06)
        CanvasCoord = GetCanvasCoord(EdgeCoord,TrussNWCoord)
        CanvasX = CanvasCoord[0]
        CanvasY = CanvasCoord[1]
        
        if DataType == "ID":
            EdgeText = Edge
        else:
            EdgeText = TrussData[DataType][Edge]
        canvas.create_text(CanvasX,CanvasY, text=EdgeText,fill="#000000")
    
def DrawCanvasRange(TrussData,TweakData):
    global ImageRanges
    TrussNWCoord = GetTrussNWCoord(TrussData)
    Layers = len(TweakData)
    ImageRanges = {}
    for n in range(Layers):
        Node = TweakData[n][0]
        
        nodes_x = len(TweakData[n][1])
        nodes_y = len(TweakData[n][2])
        
        NW = (TweakData[n][1][0],TweakData[n][2][nodes_y-1])
        SE = (TweakData[n][1][nodes_x-1],TweakData[n][2][0])
        NW = GetCanvasCoord(NW,TrussNWCoord)
        SE = GetCanvasCoord(SE,TrussNWCoord)
    
        x1 = NW[0]
        y1 = NW[1]
        x2 = SE[0]
        y2 = SE[1]
        if x2 == x1:
            ImageRangeLength = 2 
        else:
            ImageRangeLength = x2-x1
        if y2 == y1:
            ImageRangeWidth = 2 
        else:
            ImageRangeWidth = y2-y1
        
        ImageRange = Image.new("RGBA",(ImageRangeLength,ImageRangeWidth),color=(0,255,0,64))
        ImageRanges[Node] = ImageTk.PhotoImage(ImageRange)
        canvas.create_image(x1,y1,anchor="nw",image=ImageRanges[Node])


def LabelEdgeResults(TrussData,TrussResults,ResultType):
    global ImageEdgeResults
    ImageEdgeResults = {}
    TrussNWCoord = GetTrussNWCoord(TrussData)
    for Edge in TrussData["EdgeConnections"].keys():
        EdgeCoord = GetEdgeLabelCoord(TrussData, Edge,0.07)
        CanvasCoord = GetCanvasCoord(EdgeCoord,TrussNWCoord)
        CanvasX = CanvasCoord[0]
        CanvasY = CanvasCoord[1]
        
        ImageResultValue = Image.new("RGBA",(60,20), color=(255,255,255,192))
        ImageEdgeResults[Edge] = ImageTk.PhotoImage(ImageResultValue)
        canvas.create_image(CanvasX,CanvasY,anchor="center",image=ImageEdgeResults[Edge])
        
        Dp = {"AxialForces":4,"Stresses":4,"SxC":2}
        ResultValue = TrussResults[ResultType][Edge]
        ResultText = "%.4f" % round(ResultValue,4)
        canvas.create_text(CanvasX,CanvasY, text=ResultText,fill="#DF00FF",font=("Verdana",12))
        


#-------------------------------------------------View Truss-----------------------------------------------

def ViewTruss(TrussData,DataType = "ID", TweakData=[]):
    WindowSize = GetWindowSize(TrussData)
    root.title("Truss")
    root.geometry(WindowSize)
    DrawCanvasEdge(TrussData)
    DrawCanvasNode(TrussData)
    DrawCanvasRange(TrussData,TweakData)
    
    LabelNodeCoords(TrussData)
    LabelEdgeIDs(TrussData,DataType)
    canvas.pack(fill = "both",expand=1)
    root.mainloop()


def ViewTrussResults(TrussData,ResultType):
    WindowSize = GetWindowSize(TrussData)
    root.title("Truss Results")
    root.geometry(WindowSize)
    DrawCanvasEdge(TrussData)
    DrawCanvasNode(TrussData)
    
    TrussResults = GetTrussResults(TrussData)
    LabelEdgeResults(TrussData,TrussResults,ResultType)
    canvas.pack(fill = "both",expand=1)
    root.mainloop()


root = tk.Toplevel()
canvas = tk.Canvas(root)
