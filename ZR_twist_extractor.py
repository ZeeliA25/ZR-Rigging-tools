#----------------------------------------------------------------#
#						ZR Twist Extractor 						 #
#                       Author : ZeeliA                          #
#						V.2026-04-02							 #
#----------------------------------------------------------------#

# Import commands 

import maya.cmds as cmds
from ZR_matrix_constraint import *
#from ZR_matrixFreeze import * 

# ----------------------------------------------------------------
# Function : Twist extractor
# ----------------------------------------------------------------

def ZR_twist_extractor(obj, twistOrder) : 

	# find object's parent
	parentObj = cmds.listRelatives(obj, parent = 1)
	print(parentObj)

	# twist object
	twistExtractor = cmds.createNode("transform", name = f"{obj}_twist")
	cmds.parent(twistExtractor, "RIGGING")


	# create nodes
	mMatrixNode = cmds.createNode("multMatrix")
	dMatrixNode = cmds.createNode("decomposeMatrix")
	quatToEulerNode = cmds.createNode("quatToEuler")

	# connection order 
	if twistOrder == "Start" :
		cmds.connectAttr(f"{parentObj[0]}.worldMatrix[0]", f"{mMatrixNode}.matrixIn[0]")
		cmds.connectAttr(f"{obj}.worldInverseMatrix[0]", f"{mMatrixNode}.matrixIn[1]")
		cmds.connectAttr(f"{obj}.worldMatrix", f"{twistExtractor}.offsetParentMatrix")

	elif twistOrder == "End" :
		cmds.connectAttr(f"{obj}.worldMatrix[0]", f"{mMatrixNode}.matrixIn[0]")
		cmds.connectAttr(f"{parentObj[0]}.worldInverseMatrix[0]", f"{mMatrixNode}.matrixIn[1]")

		cmds.matchTransform(twistExtractor, parentObj[0])
		cmds.matchTransform(twistExtractor, obj, position = 1, rotation = 0, scale = 0)
		ZR_matrixConstraint(parentObj[0], twistExtractor)

	# other connections
	cmds.connectAttr(f"{mMatrixNode}.matrixSum", f"{dMatrixNode}.inputMatrix")
	cmds.connectAttr(f"{dMatrixNode}.outputQuatX", f"{quatToEulerNode}.inputQuatX")
	cmds.connectAttr(f"{dMatrixNode}.outputQuatW", f"{quatToEulerNode}.inputQuatW")

	cmds.connectAttr(f"{quatToEulerNode}.outputRotateX", f"{twistExtractor}.rotateX")

	# retunr du twist extractor
	return twistExtractor


# ----------------------------------------------------------------
# Twist Extractor on selection
# ----------------------------------------------------------------

def ZR_twist_extractor_selection():

	sel = cmds.ls(sl = True)

	if len(sel) != 1 :
		cmds.error("You need to select a transform !")

	else :
	    result = cmds.promptDialog(
		title = "Twist order",
		message = "Enter twist order",
		text = "Start",
		button = ("OK","Cancel"),
		defaultButton = "OK",
		cancelButton = "Cancel",
		dismissString = "Cancel")

	    if result == "OK" :
		    twistOrder = cmds.promptDialog(query = True, text = True)
		    ZR_twist_extractor(sel[0], twistOrder)

	    else :
		    cmds.error("Nothing entered")
	       

	