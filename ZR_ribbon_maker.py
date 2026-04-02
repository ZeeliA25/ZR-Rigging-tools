#----------------------------------------------------------------#
#                       ZR Ribbon Maker                          #
#                     Author : ZeeliA                            #
#                       v.2026-04-02.002                         #
#----------------------------------------------------------------#

# Import modules and commands

import maya.cmds as cmds
from ZR_nameCon import *
from ZR_matrixRivet import *
from ZR_twist_extractor import*

# ----------------------------------------------------------------
# Function : Ribbon Maker
# ----------------------------------------------------------------

def ZR_ribbon_maker(startObj, endObj, twistOrder, globalLoc) :
    
    # Prompt Dialog
    promptRibbon = cmds.promptDialog(
        title="BRA Ribbon Maker",
        message="Joint number :",
        text="5",
        style="integer",
        button=["OK", "Cancel"],
        defaultButton="OK",
        cancelButton="Cancel",
        dismissString="Cancel")

    if promptRibbon == "OK":

    	jointNumberPrompt = cmds.promptDialog(query=True, text=True)
    	jointNumber = int(jointNumberPrompt)
    	
    	if jointNumber <= 0 :
    	    cmds.error("!!! Please enter a value of 1 or more !!!")

	# Define the names

    startName = startObj.split("_")
    endName = endObj.split("_")

    # Create three curves (unless they already exist)


    startCurve = cmds.curve(degree=1, p=[(0, 1, 0), (0, -1, 0)], n = ZR_nameCon(startName[0], f"{startName[1]}Start", "curve"))

    midCurve = cmds.curve(degree=1, p=[(0, 1, 0), (0, -1, 0)], n = ZR_nameCon(endName[0], f"{endName[1]}Mid", "curve"))

    endCurve = cmds.curve(degree=1, p=[(0, 1, 0), (0, -1, 0)], n = ZR_nameCon(endName[0], f"{endName[1]}End", "curve"))

	# Place the three curves and make them follow the objects
    blendMatrixEndNode = cmds.createNode("blendMatrix")
    cmds.connectAttr(f"{startObj}.worldMatrix[0]", f"{blendMatrixEndNode}.inputMatrix")
    cmds.connectAttr(f"{endObj}.worldMatrix[0]", f"{blendMatrixEndNode}.target[0].targetMatrix")
    cmds.setAttr(f"{blendMatrixEndNode}.target[0].rotateWeight", 0)

    cmds.connectAttr(f"{startObj}.worldMatrix[0]", f"{startCurve}.offsetParentMatrix", force = 1)
    cmds.connectAttr(f"{blendMatrixEndNode}.outputMatrix", f"{endCurve}.offsetParentMatrix", force = 1)

    blendMatrixNode = cmds.createNode("blendMatrix")
    
    cmds.connectAttr(f"{startCurve}.worldMatrix[0]", f"{blendMatrixNode}.inputMatrix", force = 1)
    cmds.connectAttr(f"{endCurve}.worldMatrix[0]", f"{blendMatrixNode}.target[0].targetMatrix", force = 1)
    cmds.connectAttr(f"{blendMatrixNode}.outputMatrix", f"{midCurve}.offsetParentMatrix", force = 1)
    cmds.setAttr(f"{blendMatrixNode}.target[0].weight", 0.5)
    cmds.setAttr(f"{blendMatrixNode}.target[0].rotateWeight", 0)

    # Place the curves inside the hierarchy
    if cmds.objExists("RIBBONS_CRV") :
        cmds.parent(startCurve, "RIBBONS_CRV")
        cmds.parent(midCurve, "RIBBONS_CRV")
        cmds.parent(endCurve, "RIBBONS_CRV")


	# Create the nurbSurface (linear)
    ribbonBase = cmds.loft(startCurve, midCurve, endCurve, ch = 1, u = 1, d = 1)

	# Rebuild the surface (U : degree 1, V : degree 3)
    cmds.rebuildSurface(ribbonBase[0], du = 3, dv = 1, kr=0, su=3, sv = 0, ch = 1, rpo = 1)
    # Rebuild the surface (U : degree 1, V : degree 3 +  spans)
    cmds.rebuildSurface(ribbonBase[0], du = 3, dv = 1, kr=0, su=6, sv = 0, ch = 1, rpo = 1)

    # Rename the ribbon
    ribbon = cmds.rename(ribbonBase[0], f"{endObj}_ribbon")

    # Find the rebuilt ribbon's shape
    ribbonShapeList = cmds.listRelatives(ribbon, shapes=1)
    surfaceShape = ribbonShapeList[0]

    # Place the ribbon inside the hierarchy
    if cmds.objExists("RIBBONS_SRF") :
        cmds.parent(ribbon, "RIBBONS_SRF")

    # Twist Extractor
    if twistOrder == "Start" :
        twistExtractor = ZR_twist_extractor(startObj, "Start")

        # Needs update for the start twist 
        upVector = cmds.spaceLocator(name = ZR_nameCon(startName[0], startName[1], "locator"))
        cmds.matchTransform(upVector, startObj)

        if startName[0] == "L" :
            cmds.move(0,5,0, upVector[0], r = True, os = True, wd = True)

        elif startName[0] == "R" :
            cmds.move(0,-5,0, upVector[0], r = True, os = True, wd = True)

        aimMatrixNode = cmds.createNode("aimMatrix")
        cmds.connectAttr( f"{globalLoc}.worldMatrix[0]", f"{aimMatrixNode}.inputMatrix")
        cmds.connectAttr(f"{endObj}.worldMatrix[0]", f"{aimMatrixNode}.primaryTargetMatrix")
        cmds.connectAttr(f"{upVector[0]}.worldMatrix[0]", f"{aimMatrixNode}.secondaryTargetMatrix")
        cmds.setAttr(f"{aimMatrixNode}.secondaryMode", 1)
        
        if startName[0] == "R" :
            cmds.setAttr(f"{aimMatrixNode}.primaryInputAxisX", -1)
            cmds.setAttr(f"{aimMatrixNode}.secondaryInputAxisY", -1)

        cmds.connectAttr(f"{aimMatrixNode}.outputMatrix", f"{startCurve}.offsetParentMatrix", force = 1)

        blendMatrixStartNode = cmds.createNode("blendMatrix")
        cmds.connectAttr(f"{aimMatrixNode}.outputMatrix", f"{blendMatrixStartNode}.inputMatrix")
        cmds.connectAttr(f"{endObj}.worldMatrix[0]", f"{blendMatrixStartNode}.target[0].targetMatrix")
        cmds.setAttr(f"{blendMatrixStartNode}.target[0].scaleWeight", 0)
        cmds.setAttr(f"{blendMatrixStartNode}.target[0].rotateWeight", 0)
        cmds.setAttr(f"{blendMatrixStartNode}.target[0].shearWeight", 0)
        cmds.connectAttr(f"{blendMatrixStartNode}.outputMatrix", f"{endCurve}.offsetParentMatrix", force = 1)



    elif twistOrder == "End" :
        twistExtractor = ZR_twist_extractor(endObj, "End")

    for number in range(1, jointNumber+1) :

        #Create a joint for each iteration of jointNumber
        ribbonJoint = cmds.createNode("joint", n = ZR_nameCon(startName[0], startName[1]+ "Ribbon" + str(number), "joint"))

        rivetMatrix = ZR_matrixRivet(surfaceShape,(number*(1/(jointNumber+1))))
        
        cmds.connectAttr(f"{rivetMatrix}.output", f"{ribbonJoint}.offsetParentMatrix")

        # Twist connections
        if twistOrder == "Start" :
            jointTwistCoef = ((number*(1/(jointNumber+1)))*(-1))
        elif twistOrder == "End" :
            jointTwistCoef = (number*(1/(jointNumber+1)))    
        
        twistCoefNode = cmds.createNode("multDoubleLinear")
        cmds.connectAttr((f"{twistExtractor}.rotateX"), (f"{twistCoefNode}.input1"))
        cmds.setAttr(f"{twistCoefNode}.input2", jointTwistCoef)
        cmds.connectAttr(f"{twistCoefNode}.output", f"{ribbonJoint}.rotateX")
        
        # Scale connections
        
        cmds.connectAttr("C_main_ctl.scale", f"{ribbonJoint}.scale")


        # Place the joint inside the hierarchy
        if cmds.objExists("RIBBONS_JNT") == 1 :
            cmds.parent(ribbonJoint, "RIBBONS_JNT")

    # Return the three curves
    return(startCurve, midCurve, endCurve)

# ----------------------------------------------------------------
# Function : Create a ribbon on selection
# ----------------------------------------------------------------

def ZR_ribbonSelection ():

	sel = cmds.ls(sl = True)

    # Define start and end of the ribbon using the selection

	if len(sel) != 2 :
		cmds.error("You need to select a start and end object")

	else : 
		startObj = sel[0]
		endObj = sel[1]
		ZR_ribbon_maker(startObj, endObj)