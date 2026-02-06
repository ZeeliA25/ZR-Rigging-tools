#--------------------------------------------------------------#
#                       ZR Rotate Plane                        #
#                     Author : ZeeliA                          #
#                v.2026-02-06-001 / Maya 2023.1                #
#--------------------------------------------------------------#

import maya.cmds as cmds
from ZR_nameCon import *
from ZR_makeControler import *
from ZR_displayCurve import *
from ZR_rotatePlane import * 

# -------------------------------------------------------------------------------------------
# Fonction : Create a plane to place pole vector
# -------------------------------------------------------------------------------------------


def ZR_rotatePlane(pointA, pointB, pointC) :

    # If group "PREVIZ" doesn't exists, create it
    if cmds.objExists("PREVIZ") != 1 :
        cmds.group(em = 1, n = "PREVIZ")

    # Creation of preview locator and it's placement group
    previzLoc = cmds.spaceLocator(name = (ZR_nameCon("", "previz", "locator")))
    previzGrp = cmds.group(em = 1, n = (ZR_nameCon("", "previz", "group")))
 
    # Creation of the plane
    previzPlane = cmds.polyCreateFacet(p=[(0,0,0), (0,0,0), (0,0,0)])
    # Rangement
    cmds.parent(previzLoc[0], previzGrp)
    cmds.parent(previzGrp, "PREVIZ")
    cmds.parent(previzPlane, "PREVIZ")
    
    # Creation of nodes
    aimMatrixNode = cmds.createNode("aimMatrix")
    cmds.setAttr(f"{aimMatrixNode}.secondaryMode",1)
        
    distanceNode = cmds.createNode("distanceBetween")
        
    multNodeX = cmds.createNode("multDoubleLinear")
    cmds.setAttr(f"{multNodeX}.input2", 0.5) 
      
    multNodeY = cmds.createNode("multDoubleLinear")
    cmds.setAttr(f"{multNodeY}.input2", 0.75)  
        
    decomposeMatrixA = cmds.createNode("decomposeMatrix")
    decomposeMatrixB = cmds.createNode("decomposeMatrix")
    decomposeMatrixC = cmds.createNode("decomposeMatrix")

    # Connections
    cmds.connectAttr(f"{pointA}.worldMatrix[0]", f"{distanceNode}.inMatrix1")
    cmds.connectAttr(f"{pointA}.worldMatrix[0]", f"{aimMatrixNode}.inputMatrix")
    cmds.connectAttr(f"{pointA}.worldMatrix[0]", f"{decomposeMatrixA}.inputMatrix")
    
    cmds.connectAttr(f"{pointB}.worldMatrix[0]", f"{aimMatrixNode}.secondaryTargetMatrix")
    
    cmds.connectAttr(f"{pointC}.worldMatrix[0]", f"{distanceNode}.inMatrix2")
    cmds.connectAttr(f"{pointC}.worldMatrix[0]", f"{aimMatrixNode}.primaryTargetMatrix")
    cmds.connectAttr(f"{pointC}.worldMatrix[0]", f"{decomposeMatrixC}.inputMatrix")
    
    cmds.connectAttr(f"{distanceNode}.distance", f"{multNodeX}.input1")
    cmds.connectAttr(f"{distanceNode}.distance", f"{multNodeY}.input1")
    
    cmds.connectAttr(f"{multNodeX}.output", f"{previzLoc[0]}.translateX")
    cmds.connectAttr(f"{multNodeY}.output", f"{previzLoc[0]}.translateY")
    
    cmds.connectAttr(f"{previzLoc[0]}.worldMatrix[0]", f"{decomposeMatrixB}.inputMatrix")
    
    cmds.connectAttr(f"{decomposeMatrixA}.outputTranslate", f"{previzPlane[0]}.pnts[0]" )
    cmds.connectAttr(f"{decomposeMatrixB}.outputTranslate", f"{previzPlane[0]}.pnts[1]" )
    cmds.connectAttr(f"{decomposeMatrixC}.outputTranslate", f"{previzPlane[0]}.pnts[2]")

    cmds.connectAttr(f"{aimMatrixNode}.outputMatrix", f"{previzGrp}.offsetParentMatrix")

    # Set locator look
    # Lock Channels
    # Selection (and Return) of locator
 
 
# -------------------------------------------------------------------------------------------
# Create rotate plane on selection
# -------------------------------------------------------------------------------------------
 

def ZR_rotatePlaneSelection() :

    # Define the 3 points with selection
    selList = cmds.ls(sl=True)
    
    if len(selList) == 0:
        cmds.error("Nothing is selected dude!")
        
    pointA = selList[0]
    pointB = selList[1]
    pointC = selList[2]
    
    ZR_rotatePlane(pointA, pointB, pointC)