#--------------------------------------------------------------#
#                       ZR IKFK		                           #
#                     Author : ZeeliA                          #
#                v.2026-04-02-004 / Maya 2023.3.1              #
#--------------------------------------------------------------#

# Import modules

from ZR_nameCon import *
from ZR_make_controler import *
from ZR_display_curve import *
from ZR_rotatePlane import *
from ZR_ribbon_maker import *
from ZR_reverse_foot import *

#---------------------------------------------------------------
# Identify different parts of the IKFK system
#---------------------------------------------------------------

# List selection 

sel = cmds.ls(sl=True, type = "joint")

# Check only one object is selected

if len(sel) != 1 :
    cmds.error("Too many arguments selected")

else :
    result = cmds.promptDialog(
    title = "Limb type",
    message = "Enter limb type",
    text = "arm",
    button = ("OK", "Cancel"),
    defaultButton = "OK",
    cancelButton = "Cancel",
    dismissString = "Cancel")

    if result == "OK" :
        limbType = cmds.promptDialog(query = True, text = True)
    else :
        cmds.error("Nothing entered")

dad = sel[0]

# Look for selection's children (elbow and wrist)

son = cmds.listRelatives(dad, c = True)
grandson = cmds.listRelatives(son, c = True)
cousin = cmds.listRelatives(grandson, c = True)
cousinEnd = cmds.listRelatives(cousin, c = True)
grandsonEnd = cmds.listRelatives(cousinEnd, c = True)

# Look for selection's parent (clavicle)

grandDad = cmds.listRelatives(dad, p = True)

# Determine object's position in space (left, right or center)

spacePosition = cmds.xform(dad, query=1, t=1, ws=1 )
side = ""

if spacePosition[0] > 0 :
    side = "left"
elif spacePosition[0] < 0 :
    side = "right"
else :
	side = ""

# Determine if it's an arm or a leg 

if limbType == "arm" :
	dadName = "shoulder"
	sonName = "elbow"
	grandsonName = "wrist"
	limb = "hand"

if limbType == "leg" :
	dadName = "hip"
	sonName = "knee"
	grandsonName = "ankle"
	limb = "foot"
	digit = "toes"  


# Rename skinning joints
dadSK = cmds.rename(dad, ZR_nameCon(side, dadName, "skin"))
sonSK = cmds.rename(son, ZR_nameCon(side, sonName, "skin"))
grandsonSK = cmds.rename(grandson, ZR_nameCon(side, grandsonName, "skin"))

if limbType == "leg" :
    cousinSK = cmds.rename(cousin, ZR_nameCon(side, digit, "skin"))
    cousinEndSK = cmds.rename(cousinEnd, ZR_nameCon(side, digit, "skinEnd"))
    grandsonEndSK = cmds.rename(grandsonEnd, ZR_nameCon(side, grandsonName, "skinEnd"))


# Get main controller's size
globalSize = cmds.getAttr(f"C_main_ctl.GEO_SIZE")

#---------------------------------------------------------------
# Creation of global controller
#---------------------------------------------------------------

# Creation of Global locator
globalLoc = cmds.spaceLocator(n = ZR_nameCon(side, limbType, "locator"))

# Create IKFK attribute / Match transform 
IKFK = cmds.addAttr(globalLoc[0], k = True, ln="IKFK", defaultValue=1, minValue=0, maxValue=1, at = "float")
cmds.matchTransform(globalLoc[0], dadSK)

# Parent locator to "RIGGING" group if it exists
if (cmds.objExists("RIGGING")) == 1 :
	cmds.parent(globalLoc[0], "RIGGING")

# Constraint global locator by clavicle 
cmds.parentConstraint(grandDad[0], globalLoc, mo = 1)

#---------------------------------------------------------------
# FK system
#---------------------------------------------------------------

# Creation of controllers for : shoulder / elbow / wrist
dadCtlBase = ZR_make_controler(dadSK, circle_shape)
sonCtlBase = ZR_make_controler(sonSK, circle_shape)
grandsonCtlBase = ZR_make_controler(grandsonSK, circle_shape)

if limbType == "leg" :
    cousinCtlBase = ZR_make_controler(cousinSK, half_circle)


# Rename FK controllers
dadCtl = cmds.rename(dadCtlBase[0], ZR_nameCon(side, dadName, "controller"))
sonCtl = cmds.rename(sonCtlBase[0], ZR_nameCon(side, sonName, "controller"))
grandsonCtl = cmds.rename(grandsonCtlBase[0], ZR_nameCon(side, grandsonName, "controller"))

if limbType == "leg" :
    cousinCtl = cmds.rename(cousinCtlBase[0], ZR_nameCon(side, digit, "controller"))

# Rename FK placement groups 
dadGrp = cmds.rename(dadCtlBase[1], ZR_nameCon(side, dadName, "group"))
sonGrp = cmds.rename(sonCtlBase[1], ZR_nameCon(side, sonName, "group"))
grandsonGrp = cmds.rename(grandsonCtlBase[1], ZR_nameCon(side, grandsonName, "group"))

if limbType == "leg" :
    cousinGrp = cmds.rename(cousinCtlBase[1], ZR_nameCon(side, digit, "group"))

# Creation of FK pole vector
FKpvBase = ZR_make_controler(sonSK, sphere_shape)
FKpvCtl = cmds.rename(FKpvBase[0], ZR_nameCon(side, f"FK{limbType}PV", "controller"))
FKpvGrp = cmds.rename(FKpvBase[1], ZR_nameCon(side, f"FK{limbType}PV", "group"))

cmds.matchTransform(FKpvGrp, FKpvCtl)

# Place FK pole vector
ZR_rotatePlane(dadSK, sonSK, grandsonSK)
cmds.matchTransform(FKpvGrp, "previz_loc")

# FK hierarchy 
cmds.parent(sonGrp, dadCtl)
cmds.parent(grandsonGrp, sonCtl)
cmds.parent(FKpvGrp, sonCtl)

if limbType == "leg" :
    cmds.parent(cousinGrp, grandsonCtl)

# Hide FK pole vector 
cmds.setAttr(f"{FKpvGrp}.visibility", 0)

# Constraint shoulder group with clavicle
cmds.parentConstraint(grandDad, dadGrp, mo=1)

# Shoulder Follow World attribute
if limbType == "arm" :
    cmds.addAttr(dadCtl, k=1, ln="Follow_World", defaultValue=1, minValue=0, maxValue=1)

# Orient constraint between world and chest

if (cmds.objExists("worldFollow_loc")) :
    worldLoc = "worldFollow_loc"
else :
    worldLoc = cmds.spaceLocator(n=ZR_nameCon("","worldFollow","locator"))
    cmds.parent(worldLoc, "RIGGING")
    
if (cmds.objExists("chestFollow_loc")) :
    chestLoc = "chestFollow_loc"
else :
    chestLoc = cmds.spaceLocator(n=ZR_nameCon("","chestFollow","locator"))
    chest = cmds.listRelatives(grandDad, p = True)
    cmds.matchTransform(chestLoc, chest[0], pos=True, rot=False)
    cmds.parentConstraint(chest[0], chestLoc, mo = 1)
    cmds.parent(chestLoc, "RIGGING")
    
if limbType == "arm" :
    offsetOrientFK = cmds.group(em = 1, name = ZR_nameCon(side, f"{limbType}offsetOrient", "group"))
    cmds.matchTransform(offsetOrientFK, dadCtl)
    cmds.parent(offsetOrientFK, dadGrp)
    cmds.parent(dadCtl, offsetOrientFK)
    followConstraint = cmds.orientConstraint(worldLoc, chestLoc, offsetOrientFK, mo=1) #only when limb is an arm
    reverseNode = cmds.createNode("reverse")
    cmds.connectAttr(f"{dadCtl}.Follow_World", f"{reverseNode}.inputX")
    cmds.connectAttr(f"{reverseNode}.outputX", f"{followConstraint[0]}.chestFollow_locW1.")
    cmds.connectAttr(f"{dadCtl}.Follow_World", f"{followConstraint[0]}.worldFollow_locW0.") 


# Proxy atribute IKFK on FK controllers
cmds.addAttr(dadCtl, ln="IKFK", pxy= f"{globalLoc[0]}.IKFK")
cmds.addAttr(sonCtl, ln="IKFK", pxy= f"{globalLoc[0]}.IKFK")
cmds.addAttr(grandsonCtl, ln="IKFK", pxy= f"{globalLoc[0]}.IKFK")

if limbType == "leg" :
    cmds.addAttr(cousinCtl, ln="IKFK", pxy = f"{globalLoc[0]}.IKFK")

#----------------------------------------------------------------
# IK System
#----------------------------------------------------------------
 
# Create IK chain by duplicating the FK joints and deleting the extra joints
 
IKchain = cmds.duplicate(dadSK, rc= 1 )

counter = 0

if limbType == "arm" :
    for IKjoint in IKchain :
        if counter < 3 :
            counter = counter+1
        else :
            if cmds.objExists(IKjoint) == 1 :
                cmds.delete(IKjoint)

if limbType == "leg" :
    for IKjoint in IKchain :
        if counter < 5 :
            counter = counter+1
        else :
            if cmds.objExists(IKjoint) == 1 :
                cmds.delete(IKjoint)

# Rename IK joints
dadIK = cmds.rename(IKchain[0], ZR_nameCon(side, dadName, "rig"))
sonIK = cmds.rename(IKchain[1], ZR_nameCon(side, sonName, "rig"))
grandsonIK = cmds.rename(IKchain[2], ZR_nameCon(side, grandsonName, "rig"))

if limbType == "leg" :
    cousinIK = cmds.rename(IKchain[3], ZR_nameCon(side, digit, "rig"))
    cousinEndIK = cmds.rename(IKchain[4], ZR_nameCon(side, digit, "rigEnd"))
    
# Parent IK chain to au global locator
cmds.parent(dadIK, globalLoc[0])

# Create hand IK controller
handIKbase = ZR_make_controler(grandsonIK, cube)
handIKctl = cmds.rename(handIKbase[0], ZR_nameCon(side, limb, "controller"))
handIKgrp = cmds.rename(handIKbase[1], ZR_nameCon(side, limb, "group"))

# Create pole vector
pvBase = ZR_make_controler(sonIK, sphere_shape)
pvCtl = cmds.rename(pvBase[0], ZR_nameCon(side, f"{limbType}PV", "controller"))
pvGrp = cmds.rename(pvBase[1], ZR_nameCon(side, f"{limbType}PV", "group"))

cmds.matchTransform(pvGrp, pvCtl)

# Place pole Vector
cmds.matchTransform(pvGrp, "previz_loc")
cmds.delete("PREVIZ")


# Constrain pole Vector
mainCtl = "C_main_ctl"
cmds.addAttr(pvCtl, longName = "Follow_Main", attributeType = "float", k=1, min = 0, max=1, defaultValue=1)
pvParentConstraint = cmds.parentConstraint(mainCtl, handIKctl, pvGrp, mo=1)
cmds.setAttr(f"{pvParentConstraint[0]}.interpType", 2)

reverseNode = cmds.createNode("reverse")

cmds.connectAttr(f"{pvCtl}.Follow_Main", f"{pvParentConstraint[0]}.{mainCtl}W0")
cmds.connectAttr(f"{pvCtl}.Follow_Main", f"{reverseNode}.inputX")
cmds.connectAttr(f"{reverseNode}.outputX", f"{pvParentConstraint[0]}.{handIKctl}W1")

# Create display curve
curveIKPv = ZR_display_curve(pvCtl, sonIK)
cmds.connectAttr(f"{globalLoc[0]}.IKFK", f"{curveIKPv}.visibility")

# Add the attribute "Follow World" to the IK hand controller
cmds.addAttr(handIKctl, ln = "Follow_World", k=1, defaultValue=1, minValue=0, maxValue=1)

# Blend constraint between the world and IK hand
offsetOrientIK = cmds.group(em = 1, name = ZR_nameCon(side, f"{limbType}offsetOrientIK", "group"))
cmds.matchTransform(offsetOrientIK, handIKgrp)
cmds.parent(offsetOrientIK, handIKgrp)
cmds.parent(handIKctl, offsetOrientIK)
followIK = cmds.orientConstraint(worldLoc, offsetOrientIK, mo=1)
cmds.connectAttr(f"{handIKctl}.Follow_World", f"{followIK[0]}.worldFollow_locW0.")
 
# Create IK handle, parent it to the controller and hide it
ikRpHandle = cmds.ikHandle(n=ZR_nameCon(side, f"{limbType}IKRP", 'handle') , startJoint=dadIK , endEffector=grandsonIK, solver="ikRPsolver")
cmds.parent(ikRpHandle[0], handIKctl)

cmds.setAttr(f"{ikRpHandle[0]}.visibility", 0, lock=1)
cmds.setAttr(f"{ikRpHandle[0]}.translate", lock=1)
cmds.setAttr(f"{ikRpHandle[0]}.rotate", lock=1)
cmds.setAttr(f"{ikRpHandle[0]}.scale", lock=1)

# Constrain IK handle to the pole vector
cmds.poleVectorConstraint(pvCtl, ikRpHandle[0])
 
# Orient constraint hand joint by IK hand controller

cmds.orientConstraint(handIKctl, grandsonIK)

# Proxy of IKFK attribute from "GLOBAL" locator to the IK controllers

cmds.addAttr(handIKctl, ln="IKFK", pxy= f"{globalLoc[0]}.IKFK")
cmds.addAttr(pvCtl, ln="IKFK", pxy= f"{globalLoc[0]}.IKFK")
 
#----------------------------------------------------------------
# Reverse foot
#----------------------------------------------------------------
# Create IK handle (single chain) for the foot 

if limbType == "leg" :
    footIKSCHandle = cmds.ikHandle(n = ZR_nameCon(side, "footIKSC", "handle"), startJoint = grandsonIK, endEffector = cousinIK, solver = "ikSCsolver")
    toesIKSCHandle = cmds.ikHandle(n = ZR_nameCon(side, "toesIKSC", "handle"), startJoint = cousinIK, endEffector = cousinEndIK, solver = "ikSCsolver")

    reverse_foot = ZR_reverse_foot(side, handIKctl)

    cmds.parent(toesIKSCHandle[0], reverse_foot[0])
    cmds.parent(footIKSCHandle[0], reverse_foot[1])
    cmds.parent(ikRpHandle[0], reverse_foot[2])

    cmds.setAttr(f"{reverse_foot[3]}.visibility", 0)


#----------------------------------------------------------------
# Stretch :)
#----------------------------------------------------------------

cmds.addAttr(handIKctl, ln = "Stretch_Max", k = 1, min = 1, max = 10)

distance = cmds.createNode("distanceBetween")
cmds.connectAttr(f"{globalLoc[0]}.worldMatrix[0]", f"{distance}.inMatrix1")
cmds.connectAttr(f"{handIKctl}.worldMatrix", f"{distance}.inMatrix2")

mainScale = cmds.createNode("floatMath")
cmds.setAttr(f"{mainScale}.operation", 2)

cmds.connectAttr(f"{mainCtl}.scaleX", f"{mainScale}.floatA")

lengthA = cmds.getAttr(f"{sonIK}.translateX")
lengthB = cmds.getAttr(f"{grandsonIK}.translateX")
armLength = (lengthA + lengthB)
if  armLength < 0 :
	armLength = (lengthA + lengthB)*(-1)

cmds.setAttr(f"{mainScale}.floatB", armLength)
coefStretch = cmds.createNode("multiplyDivide")
cmds.setAttr(f"{coefStretch}.operation", 2)
cmds.connectAttr(f"{distance}.distance", f"{coefStretch}.input1X")
cmds.connectAttr(f"{mainScale}.outFloat", f"{coefStretch}.input2X")

clamp = cmds.createNode("clamp")
cmds.setAttr(f"{clamp}.minR", 1)
cmds.connectAttr(f"{coefStretch}.outputX", f"{clamp}.inputR")
cmds.connectAttr(f"{handIKctl}.Stretch_Max", f"{clamp}.maxR")

multiplySon = cmds.createNode("floatMath")
cmds.setAttr(f"{multiplySon}.operation", 2)
cmds.setAttr(f"{multiplySon}.floatB", lengthA)
cmds.connectAttr(f"{clamp}.outputR", f"{multiplySon}.floatA")
cmds.connectAttr(f"{multiplySon}.outFloat", f"{sonIK}.translateX")

multiplyGrandson = cmds.createNode("floatMath")
cmds.setAttr(f"{multiplyGrandson}.operation", 2)
cmds.setAttr(f"{multiplyGrandson}.floatB", lengthB)
cmds.connectAttr(f"{clamp}.outputR", f"{multiplyGrandson}.floatA")
cmds.connectAttr(f"{multiplyGrandson}.outFloat", f"{grandsonIK}.translateX")

#---------------------------------------------------------------
# Blend system
#---------------------------------------------------------------

# Parent constraint joints to the controllers
blendDad = cmds.parentConstraint(dadCtl, dadIK, dadSK)
cmds.setAttr(f"{blendDad[0]}.interpType", 2)

blendSon = cmds.parentConstraint(sonCtl, sonIK, sonSK)
cmds.setAttr(f"{blendSon[0]}.interpType", 2)

blendGrandson = cmds.parentConstraint(grandsonCtl, grandsonIK, grandsonSK)
cmds.setAttr(f"{blendGrandson[0]}.interpType", 2)

if limbType == "leg" :
    blendCousin = cmds.parentConstraint(cousinCtl, cousinIK, cousinSK)
    cmds.setAttr(f"{blendCousin[0]}.interpType", 2)



reverseNode = cmds.createNode("reverse")
cmds.connectAttr(f"{globalLoc[0]}.IKFK", f"{reverseNode}.inputX")
cmds.connectAttr(f"{reverseNode}.outputX", f"{blendDad[0]}.{ dadCtl}W0")
cmds.connectAttr(f"{globalLoc[0]}.IKFK", f"{blendDad[0]}.{dadIK}W1")

cmds.connectAttr(f"{reverseNode}.outputX",f"{ blendSon[0]}.{sonCtl}W0")
cmds.connectAttr(f"{globalLoc[0]}.IKFK", f"{blendSon[0]}.{sonIK}W1")

cmds.connectAttr(f"{reverseNode}.outputX", f"{blendGrandson[0]}.{grandsonCtl}W0")
cmds.connectAttr(f"{globalLoc[0]}.IKFK", f"{blendGrandson[0]}.{grandsonIK}W1")

if limbType == "leg" :
    cmds.connectAttr(f"{reverseNode}.outputX", f"{blendCousin[0]}.{cousinCtl}W0")
    cmds.connectAttr(f"{globalLoc[0]}.IKFK", f"{blendCousin[0]}.{cousinIK}W1")


cmds.connectAttr(f"{globalLoc[0]}.IKFK", f"{handIKgrp}.visibility")
cmds.connectAttr(f"{globalLoc[0]}.IKFK", f"{pvGrp}.visibility")

cmds.connectAttr(f"{reverseNode}.outputX", f"{dadGrp}.visibility")

ctrlList = cmds.ls(dadCtl, sonCtl, grandsonCtl, FKpvCtl, handIKctl, pvCtl, dadIK, sonIK, grandsonIK)

for ctrl in ctrlList :
    cmds.addAttr(ctrl, ln = "GLOBAL", dataType = "string")
    cmds.setAttr(f"{ctrl}.GLOBAL", globalLoc[0], type = "string", lock = 1)

#---------------------------------------------------------------
# Ribbon system
#---------------------------------------------------------------

# Create the ribbon 
dadCurves = ZR_ribbon_maker(dadSK, sonSK, "Start", globalLoc[0])
sonCurves = ZR_ribbon_maker(sonSK, grandsonSK, "End", globalLoc[0])

# Create the ribbon controllers
dadRibCtlbase = ZR_make_controler(dadCurves[1], square)
sonRibCtlBase = ZR_make_controler(sonCurves[1], square)

dadRibCtl = cmds.rename(dadRibCtlbase[0], ZR_nameCon(side, f"{dadName}Ribbon", "controller"))
dadRibGrp = cmds.rename(dadRibCtlbase[1], ZR_nameCon(side, f"{dadName}Ribbon", "group"))

sonRibCtl = cmds.rename(sonRibCtlBase[0], ZR_nameCon(side, f"{sonName}Ribbon", "controller"))
sonRibGrp = cmds.rename(sonRibCtlBase[1], ZR_nameCon(side, f"{sonName}Ribbon", "group"))

# List connections
blendMatrixDad = cmds.listConnections((f"{dadCurves[1]}.offsetParentMatrix"), source = 1, type = "blendMatrix")
blendMatrixSon = cmds.listConnections((f"{sonCurves[1]}.offsetParentMatrix"), source = 1, type = "blendMatrix")

# Connect blend matrix nodes to groups 
parentGrp = cmds.listRelatives(dadRibGrp, parent = 1)

multMatrixRibDad = cmds.createNode("multMatrix")
multMatrixRibSon = cmds.createNode("multMatrix")

cmds.connectAttr((f"{blendMatrixDad[0]}.outputMatrix"), (f"{multMatrixRibDad}.matrixIn[0]"))
cmds.connectAttr((f"{blendMatrixSon[0]}.outputMatrix"), (f"{multMatrixRibSon}.matrixIn[0]"))

cmds.connectAttr(f"{parentGrp[0]}.worldInverseMatrix[0]", f"{multMatrixRibDad}.matrixIn[1]")
cmds.connectAttr(f"{parentGrp[0]}.worldInverseMatrix[0]", f"{multMatrixRibSon}.matrixIn[1]")

cmds.connectAttr(f"{multMatrixRibDad}.matrixSum", f"{dadRibGrp}.offsetParentMatrix")
cmds.connectAttr(f"{multMatrixRibSon}.matrixSum", f"{sonRibGrp}.offsetParentMatrix")

cmds.setAttr(f"{dadRibGrp}.translate", 0,0,0)
cmds.setAttr(f"{dadRibGrp}.rotate", 0,0,0)

cmds.setAttr(f"{sonRibGrp}.translate", 0,0,0)
cmds.setAttr(f"{sonRibGrp}.rotate", 0,0,0)

# Connect controllers to curves 
cmds.connectAttr(f"{dadRibCtl}.translate", f"{dadCurves[1]}.translate")
cmds.connectAttr(f"{dadRibCtl}.rotate", f"{dadCurves[1]}.rotate")
cmds.connectAttr(f"{sonRibCtl}.translate", f"{sonCurves[1]}.translate")
cmds.connectAttr(f"{sonRibCtl}.rotate", f"{sonCurves[1]}.rotate")

	
#---------------------------------------------------------------
#META DATA IKFK
#---------------------------------------------------------------
	
cmds.addAttr(globalLoc[0], ln = "Limb_Type", dataType = "string")
cmds.setAttr(f"{globalLoc[0]}.Limb_Type", limbType, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "FK_ctl_01", dataType = "string")
cmds.setAttr(f"{globalLoc[0]}.FK_ctl_01", dadCtl, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "FK_ctl_02", dataType = "string")
cmds.setAttr(f"{globalLoc[0]}.FK_ctl_02", sonCtl, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "FK_ctl_03", dataType = "string")
cmds.setAttr(f"{globalLoc[0]}.FK_ctl_03", grandsonCtl, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "FK_poleVector", dataType = "string")
cmds.setAttr(f"{globalLoc[0]}.FK_poleVector", FKpvCtl, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "IK_ctl_01", dataType = "string")
cmds.setAttr(f"{globalLoc[0]}.IK_ctl_01", handIKctl, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "IK_poleVector", dataType = "string")
cmds.setAttr(f"{globalLoc[0]}.IK_poleVector", pvCtl, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "IK_jnt_01", dataType = "string")
cmds.setAttr(f"{globalLoc[0]}.IK_jnt_01", dadIK, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "IK_jnt_02", dataType = "string")
cmds.setAttr(f"{globalLoc[0]}.IK_jnt_02", sonIK, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "IK_jnt_03", dataType = "string")
cmds.setAttr(f"{globalLoc[0]}.IK_jnt_03", grandsonIK, type = "string", lock=1)


def ZR_IKFK_selection():

    # List selection 
    sel = cmds.ls(sl=True, type = "joint")

    # Check if only one object is selected
    if len(sel) != 1 :
        cmds.error("Too many arguments selected")

    else :
        selected_joint = sel[0]
        ZR_IKFK(selected_joint)
