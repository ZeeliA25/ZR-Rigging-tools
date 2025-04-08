from nameCon import *

import maya.cmds as cmds

def ZR_displayCurve(startObject, endObject) :

	#creer la curve en linear, la renommer
	curveBase = cmds.curve(d=1, p=[(0, 0, 0), (2, 0, 0)] )
	displayCurve = cmds.rename(curveBase, nameCon("", startObject, "curve"))

	#trouver la shape
	curveShape = cmds.listRelatives(displayCurve, shapes=1)

	#override d' affichage
	cmds.setAttr(curveShape[0] + ".overrideEnabled", 1)
	cmds.setAttr(curveShape[0] + ".overrideDisplayType", 2)

	#creation des nodes de decompose matrix
	startMatrix = cmds.createNode("decomposeMatrix")
	endMatrix = cmds.createNode("decomposeMatrix")

	#connexions
	cmds.connectAttr(startObject + ".worldMatrix[0]", startMatrix + ".inputMatrix")
	cmds.connectAttr(startMatrix + ".outputTranslate", curveShape[0] + ".controlPoints[0]")
	cmds.connectAttr(endObject + ".worldMatrix[0]", endMatrix + ".inputMatrix")
	cmds.connectAttr(endMatrix + ".outputTranslate", curveShape[0] + ".controlPoints[1]")

	if cmds.objExists("CURVES") == 1 :
		cmds.parent(displayCurve, "CURVES")

	return displayCurve


def ZR_dispCurveSelection():
	sel = cmds.ls(sl=True)

	if len(sel) != 2 :
		cmds.error("You need to select two objects dude")

	else :
		startObject = sel[0]
		endObject = sel[1]
		ZR_displayCurve(startObject, endObject)