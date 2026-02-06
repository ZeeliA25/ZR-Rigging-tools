#--------------------------------------------------------------#
#                     ZR Display Curve                         #
#                     Author : ZeeliA                          #
#                     v.2026-02-06-001                         #
#--------------------------------------------------------------#

import maya.cmds as cmds
from nameCon import *

#---------------------------------------------------------------
# Function : Ceating a display curve between two objects
#---------------------------------------------------------------


def ZR_display_curve(startObject, endObject) :

	#Create a linear curve and rename it
	curveBase = cmds.curve(d=1, p=[(0, 0, 0), (2, 0, 0)] )
	displayCurve = cmds.rename(curveBase, nameCon("", startObject, "curve"))

	#Find it's shape
	curveShape = cmds.listRelatives(displayCurve, shapes=1)

	#Display override
	cmds.setAttr(f"{curveShape[0]}.overrideEnabled", 1)
	cmds.setAttr(f"{curveShape[0]}.overrideDisplayType", 2)

	#Create decompose matrix nodes
	startMatrix = cmds.createNode("decomposeMatrix")
	endMatrix = cmds.createNode("decomposeMatrix")

	#Connections
	cmds.connectAttr(f"{startObject}.worldMatrix[0]", f"{startMatrix}.inputMatrix")
	cmds.connectAttr(f"{startMatrix}.outputTranslate", f"{curveShape[0]}.controlPoints[0]")
	cmds.connectAttr(f"{endObject}.worldMatrix[0]", f"{endMatrix}.inputMatrix")
	cmds.connectAttr(f"{endMatrix}.outputTranslate", f"{curveShape[0]}.controlPoints[1]")

	if cmds.objExists("CURVES") == 1 :
		cmds.parent(displayCurve, "CURVES")

	return displayCurve

#-------------------------------------------------------------------
# Function : Creating a display curve between two selected objects
#-------------------------------------------------------------------

def ZR_dispCurveSelection():
	sel = cmds.ls(sl=True)

	if len(sel) != 2 :
		cmds.error("You need to select two objects dude")

	else :
		startObject = sel[0]
		endObject = sel[1]
		ZR_display_curve(startObject, endObject)