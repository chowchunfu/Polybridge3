Truss Calculator
------------------------------------------------------------------------------------
Written by chowchunfu

This is a Truss Calculation Tool written in Python to execute Axial forces and stresses of some simple trusses. It aims to give you a better view of stress behavior and to enhance your truss design skills.
Using 

Required Python modules: numpy, tkinter.

------------------------------------------------------------------------------------
List of Python functions(See Example1.py to Example4.py):

ImportSampleTruss(filename):
Import the truss data from the txt file in the \SampleTruss Folder. Returns TrussData (class 'dict'). 
filename (class 'str') is the filename of the txt file.

ViewTruss(TrussData):
Generate a truss diagram and show the Node coordinates and the Edge marks.
TrussData (class 'dict') can be obtained from ImportSampleTruss(filename).

ViewTrussResults(TrussData,ResultType):
Generate a truss diagram and show the truss calculation results.
TrussData (class 'dict')
ResultType (class 'str') can be: "AxialForces", "Stresses", "SxC".

GetTweakedTrussData(TrussData,Node,x,y):
Update the coordinate of one node of the truss. Returns TrussData (class 'dict')
TrussData (class 'dict')
Node (class 'str') is the required node that you want to tweak.
x (class 'float') is the x coordinate of the updated node.
y (class 'float') is the y coordinate of the updated node.

GetNodestoIterate(Center,step,nodes):
Get the node coordinates range in one direction (x or y). Returns a list of the node coordinates (class 'list').
Center (class 'float') is the center of the node coordinate
step (class 'float') is spacing of the node coordinates. Returns only one value if the step is zero.
nodes (class 'int') is the number of node coordinates in that direction.

[(Node,XCoords,YCoords)]
Get the coordinate range of the node that you want to tweak. Returns TweakData (class 'list')
Node (class 'str') is the required node that you want to tweak.
XCoords (class 'list') is the node coordinates range in X direction.
YCoords (class 'list') is the node coordinates range in Y direction.

[(Node1,XCoords1,YCoords1),(Node2,XCoords2,YCoords2)]
Get the coordinate range of two nodes that you want to tweak simultaneously. Returns TweakData (class 'list')
Parameters similar to the above function.

ViewTruss(TrussData,TweakData):
View the coordinate range in the truss diagram. Indicated by green rectangles.
TrussData (class 'dict')
TweakData (class 'list') is the list obtained by the above two functions.

SaveIteratedResults(TrussData,TweakData):
Generates a csv file containing truss results respective to the nodes in the coordinate range.
File located in the \TrussResults\IteratedResults.csv.

SaveIteratedResultAnalysis(TrussData,TweakData):
Generates a txt file filtering the minimum values of the truss results.
File located in the \TrussResults\IteratedResultAnalysis.txt.
