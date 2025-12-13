#--------------------------------------------------------------#
#                       ZR IKFK		                           #
#                v.2025-09-28-001 / Maya 2023.3.1              #
#--------------------------------------------------------------#

# Import modules

from ZR_nameCon import *
from ZR_makeControler import *
from ZR_displayCurve import *
from ZR_rotatePlane import *
from ZR_ribbonMaker import *

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

# Look for selection's parent (clavicle)
grandDad = cmds.listRelatives(dad, p = True)

#Determine object's position in space (left, right or center)

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


# Get main controller's size

globalSize = cmds.getAttr("C_main_ctl" + ".GEO_SIZE")

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
dadCtlBase = ZR_makeControler(dadSK)
sonCtlBase = ZR_makeControler(sonSK)
grandsonCtlBase = ZR_makeControler(grandsonSK)

if limbType == "leg" :
    cousinCtlBase = ZR_makeControler(cousinSK)


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
FKpvBase = ZR_makeControler(sonSK)
print(FKpvBase[0], FKpvBase[1])
FKpvCtl = cmds.rename(FKpvBase[0], ZR_nameCon(side, "FK" + limbType + "PV", "controller"))
FKpvGrp = cmds.rename(FKpvBase[1], ZR_nameCon(side, "FK" + limbType + "PV", "group"))

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
cmds.setAttr(FKpvGrp + ".visibility", 0)

# Constraint shoulder group with clavicle
cmds.parentConstraint(grandDad, dadGrp, mo=1)

# Shoulder Follow World attribute
if limbType == "arm" :
    cmds.addAttr(dadCtl, k=1, ln="Follow_World", defaultValue=1, minValue=0, maxValue=1)

# orient constraint between world and chest

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
    offsetOrientFK = cmds.group(em = 1, name = ZR_nameCon(side, limbType + "offsetOrient", "group"))
    cmds.matchTransform(offsetOrientFK, dadCtl)
    cmds.parent(offsetOrientFK, dadGrp)
    cmds.parent(dadCtl, offsetOrientFK)
    followConstraint = cmds.orientConstraint(worldLoc, chestLoc, offsetOrientFK, mo=1) #only when limb is an arm
    reverseNode = cmds.createNode("reverse")
    cmds.connectAttr(dadCtl + ".Follow_World", reverseNode + ".inputX")
    cmds.connectAttr(reverseNode + ".outputX", followConstraint[0] + ".chestFollow_locW1.")
    cmds.connectAttr(dadCtl + ".Follow_World", followConstraint[0] + ".worldFollow_locW0.") 


# Proxy atribute IKFK on FK controllers
cmds.addAttr(dadCtl, ln="IKFK", pxy= globalLoc[0] + ".IKFK")
cmds.addAttr(sonCtl, ln="IKFK", pxy= globalLoc[0] + ".IKFK")
cmds.addAttr(grandsonCtl, ln="IKFK", pxy= globalLoc[0] + ".IKFK")

if limbType == "leg" :
    cmds.addAttr(cousinCtl, ln="IKFK", pxy = globalLoc[0] + ".IKFK")

#----------------------------------------------------------------
# IK System
#----------------------------------------------------------------
 
# Créer la chaîne de joints IK : dupliquer la chaine de skin, supprimer les doigts
 
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

# Renommer les joints IK
dadIK = cmds.rename(IKchain[0], ZR_nameCon(side, dadName, "rig"))
sonIK = cmds.rename(IKchain[1], ZR_nameCon(side, sonName, "rig"))
grandsonIK = cmds.rename(IKchain[2], ZR_nameCon(side, grandsonName, "rig"))

if limbType == "leg" :
    cousinIK = cmds.rename(IKchain[3], ZR_nameCon(side, digit, "rig"))
    cousinEndIK = cmds.rename(IKchain[4], ZR_nameCon(side, digit, "rigEnd"))
    
# Parenter la chaine IK au Locator Global
 
cmds.parent(dadIK, globalLoc[0])

# Créer le Controler IK de la main

handIKbase = ZR_makeControler(grandsonIK)
handIKctl = cmds.rename(handIKbase[0], ZR_nameCon(side, limb, "controller"))
handIKgrp = cmds.rename(handIKbase[1], ZR_nameCon(side, limb, "group"))

# Créer le PoleVector
pvBase = ZR_makeControler(sonIK)
pvCtl = cmds.rename(pvBase[0], ZR_nameCon(side, limbType + "PV", "controller"))
pvGrp = cmds.rename(pvBase[1], ZR_nameCon(side, limbType + "PV", "group"))

cmds.matchTransform(pvGrp, pvCtl)

# Placer le pole Vector

cmds.matchTransform(pvGrp, "previz_loc")
cmds.delete("PREVIZ")


# Contrainte sur le pole Vector
mainCtl = "C_main_ctl"
cmds.addAttr(pvCtl, longName = "Follow_Main", attributeType = "float", k=1, min = 0, max=1, defaultValue=1)
pvParentConstraint = cmds.parentConstraint(mainCtl, handIKctl, pvGrp, mo=1)
cmds.setAttr(pvParentConstraint[0] + ".interpType", 2)

reverseNode = cmds.createNode("reverse")

cmds.connectAttr(pvCtl + ".Follow_Main", pvParentConstraint[0] + "." + mainCtl + "W0")
cmds.connectAttr(pvCtl + ".Follow_Main", reverseNode + ".inputX")
cmds.connectAttr(reverseNode + ".outputX", pvParentConstraint[0] + "." + handIKctl + "W1")

# Créer la curve d'affichage

curveIKPv = ZR_displayCurve(pvCtl, sonIK)
cmds.connectAttr(globalLoc[0] + ".IKFK", curveIKPv + ".visibility")

# Attribut "Follow World" sur le controler de la main IK
cmds.addAttr(handIKctl, ln = "Follow_World", k=1, defaultValue=1, minValue=0, maxValue=1)

# Blend de contrainte en le monde et la main IK
offsetOrientIK = cmds.group(em = 1, name = ZR_nameCon(side, limbType + "offsetOrientIK", "group"))
cmds.matchTransform(offsetOrientIK, handIKgrp)
cmds.parent(offsetOrientIK, handIKgrp)
cmds.parent(handIKctl, offsetOrientIK)
followIK = cmds.orientConstraint(worldLoc, offsetOrientIK, mo=1)
cmds.connectAttr(handIKctl + ".Follow_World", followIK[0] + ".worldFollow_locW0.")
 
# Créer l'ikHandle et le parenter au controler, le cacher
ikRpHandle = cmds.ikHandle(n=ZR_nameCon(side, limbType + 'IKRP', 'handle') , startJoint=dadIK , endEffector=grandsonIK, solver="ikRPsolver")
cmds.parent(ikRpHandle[0], handIKctl)

cmds.setAttr(ikRpHandle[0]+".visibility", 0, lock=1)
cmds.setAttr(ikRpHandle[0]+".translate", lock=1)
cmds.setAttr(ikRpHandle[0]+".rotate", lock=1)
cmds.setAttr(ikRpHandle[0]+".scale", lock=1)

# Contraindre l'ikHandle par le Pole Vector
 
cmds.poleVectorConstraint(pvCtl, ikRpHandle[0])
 
# Contraindre en Orient le joint de main par le controler de la main IK

cmds.orientConstraint(handIKctl, grandsonIK)

#Créer un IK Handle SC pour le pied 

if limbType == "leg" :
    footIKSCHandle = cmds.ikHandle(n = ZR_nameCon(side, "footIKSC", "handle"), startJoint = grandsonIK, endEffector = cousinIK, solver = "ikSCsolver")
    toesIKSCHandle = cmds.ikHandle(n = ZR_nameCon(side, "toesIKSC", "handle"), startJoint = cousinIK, endEffector = cousinEndIK, solver = "ikSCsolver")
 
#----------------------------------------------------------------
# Stretch :)
#----------------------------------------------------------------

cmds.addAttr(handIKctl, ln = "Stretch_Max", k = 1, min = 1, max = 10)

distance = cmds.createNode("distanceBetween")
cmds.connectAttr(globalLoc[0] + ".worldMatrix[0]", distance + ".inMatrix1")
cmds.connectAttr(handIKctl + ".worldMatrix", distance + ".inMatrix2")

mainScale = cmds.createNode("floatMath")
cmds.setAttr(mainScale + ".operation", 2)

cmds.connectAttr(mainCtl + ".scaleX", mainScale + ".floatA")

lengthA = cmds.getAttr(sonIK + ".translateX")
lengthB = cmds.getAttr(grandsonIK + ".translateX")
armLength = (lengthA + lengthB)
if  armLength < 0 :
	armLength = (lengthA + lengthB)*(-1)

cmds.setAttr(mainScale+".floatB", armLength)
coefStretch = cmds.createNode("multiplyDivide")
cmds.setAttr(coefStretch + ".operation", 2)
cmds.connectAttr(distance + ".distance", coefStretch + ".input1X")
cmds.connectAttr(mainScale + ".outFloat", coefStretch + ".input2X")

clamp = cmds.createNode("clamp")
cmds.setAttr(clamp + ".minR", 1)
cmds.connectAttr(coefStretch + ".outputX", clamp + ".inputR")
cmds.connectAttr(handIKctl + ".Stretch_Max", clamp + ".maxR")

multiplySon = cmds.createNode("floatMath")
cmds.setAttr(multiplySon + ".operation", 2)
cmds.setAttr(multiplySon + ".floatB", lengthA)
cmds.connectAttr(clamp + ".outputR", multiplySon + ".floatA")
cmds.connectAttr(multiplySon + ".outFloat", sonIK + ".translateX")

multiplyGrandson = cmds.createNode("floatMath")
cmds.setAttr(multiplyGrandson + ".operation", 2)
cmds.setAttr(multiplyGrandson + ".floatB", lengthB)
cmds.connectAttr(clamp + ".outputR", multiplyGrandson + ".floatA")
cmds.connectAttr(multiplyGrandson + ".outFloat", grandsonIK + ".translateX")
 
# Proxy de l'attribut IKFK du locator "GLOBAL" sur les controlers IK
cmds.addAttr(handIKctl, ln="IKFK", pxy= globalLoc[0] + ".IKFK")
cmds.addAttr(pvCtl, ln="IKFK", pxy= globalLoc[0] + ".IKFK")

#---------------------------------------------------------------
# Blend system
#---------------------------------------------------------------

#parent constraint des controleurs aux joints

blendDad = cmds.parentConstraint(dadCtl, dadIK, dadSK)
cmds.setAttr(blendDad[0] + ".interpType", 2)

blendSon = cmds.parentConstraint(sonCtl, sonIK, sonSK)
cmds.setAttr(blendSon[0] + ".interpType", 2)

blendGrandson = cmds.parentConstraint(grandsonCtl, grandsonIK, grandsonSK)
cmds.setAttr(blendGrandson[0] + ".interpType", 2)

if limbType == "leg" :
    blendCousin = cmds.parentConstraint(cousinCtl, cousinIK, cousinSK)
    cmds.setAttr(blendCousin[0] + ".interpType", 2)



reverseNode = cmds.createNode("reverse")
cmds.connectAttr(globalLoc[0] +".IKFK", reverseNode +".inputX")
cmds.connectAttr(reverseNode +".outputX", blendDad[0] + "." + dadCtl + "W0")
cmds.connectAttr(globalLoc[0] +".IKFK", blendDad[0] + "." + dadIK + "W1")

cmds.connectAttr(reverseNode +".outputX", blendSon[0] + "." + sonCtl + "W0")
cmds.connectAttr(globalLoc[0] +".IKFK", blendSon[0] + "." + sonIK + "W1")

cmds.connectAttr(reverseNode +".outputX", blendGrandson[0] + "." + grandsonCtl + "W0")
cmds.connectAttr(globalLoc[0] +".IKFK", blendGrandson[0] + "." + grandsonIK + "W1")

if limbType == "leg" :
    cmds.connectAttr(reverseNode +".outputX", blendCousin[0] + "." + cousinCtl + "W0")
    cmds.connectAttr(globalLoc[0] +".IKFK", blendCousin[0] + "." + cousinIK + "W1")


cmds.connectAttr(globalLoc[0] + ".IKFK", handIKgrp + ".visibility")
#cmds.connectAttr(globalLoc[0] + ".IKFK", curveIKPv + ".visibility")
cmds.connectAttr(globalLoc[0] + ".IKFK", pvGrp + ".visibility")

cmds.connectAttr(reverseNode + ".outputX", dadGrp + ".visibility")

ctrlList = cmds.ls(dadCtl, sonCtl, grandsonCtl, FKpvCtl, handIKctl, pvCtl, dadIK, sonIK, grandsonIK)

for ctrl in ctrlList :
    cmds.addAttr(ctrl, ln = "GLOBAL", dataType = "string")
    cmds.setAttr(ctrl + ".GLOBAL", globalLoc[0], type = "string", lock = 1)

#---------------------------------------------------------------
# Ribbon system
#---------------------------------------------------------------

# Create the ribbon 
dadCurves = ZR_ribbonMaker(dadSK, sonSK, "Start", globalLoc[0])
sonCurves = ZR_ribbonMaker(sonSK, grandsonSK, "End", globalLoc[0])

# Create the ribbon controllers
dadRibCtlbase = ZR_makeControler(dadCurves[1])
sonRibCtlBase = ZR_makeControler(sonCurves[1])

dadRibCtl = cmds.rename(dadRibCtlbase[0], ZR_nameCon(side, dadName + "Ribbon", "controller"))
dadRibGrp = cmds.rename(dadRibCtlbase[1], ZR_nameCon(side, dadName + "Ribbon", "group"))

sonRibCtl = cmds.rename(sonRibCtlBase[0], ZR_nameCon(side, sonName + "Ribbon", "controller"))
sonRibGrp = cmds.rename(sonRibCtlBase[1], ZR_nameCon(side, sonName + "Ribbon", "group"))

# List connections
blendMatrixDad = cmds.listConnections((dadCurves[1] + ".offsetParentMatrix"), source = 1, type = "blendMatrix")
blendMatrixSon = cmds.listConnections((sonCurves[1] + ".offsetParentMatrix"), source = 1, type = "blendMatrix")

# Connect blend matrix nodes to groups 
parentGrp = cmds.listRelatives(dadRibGrp, parent = 1)

multMatrixRibDad = cmds.createNode("multMatrix")
multMatrixRibSon = cmds.createNode("multMatrix")

cmds.connectAttr((blendMatrixDad[0] + ".outputMatrix"), (multMatrixRibDad + ".matrixIn[0]"))
cmds.connectAttr((blendMatrixSon[0] + ".outputMatrix"), (multMatrixRibSon + ".matrixIn[0]"))

cmds.connectAttr(parentGrp[0]+ ".worldInverseMatrix[0]", multMatrixRibDad + ".matrixIn[1]")
cmds.connectAttr(parentGrp[0]+ ".worldInverseMatrix[0]", multMatrixRibSon + ".matrixIn[1]")

cmds.connectAttr(multMatrixRibDad + ".matrixSum", dadRibGrp + ".offsetParentMatrix")
cmds.connectAttr(multMatrixRibSon + ".matrixSum", sonRibGrp + ".offsetParentMatrix")

cmds.setAttr(dadRibGrp + ".translate", 0,0,0)
cmds.setAttr(dadRibGrp + ".rotate", 0,0,0)

cmds.setAttr(sonRibGrp + ".translate", 0,0,0)
cmds.setAttr(sonRibGrp + ".rotate", 0,0,0)

# Connect controllers to curves 
cmds.connectAttr(dadRibCtl + ".translate", dadCurves[1] + ".translate")
cmds.connectAttr(dadRibCtl + ".rotate", dadCurves[1] + ".rotate")
cmds.connectAttr(sonRibCtl + ".translate", sonCurves[1] + ".translate")
cmds.connectAttr(sonRibCtl + ".rotate", sonCurves[1] + ".rotate")

	
#---------------------------------------------------------------
#META DATA IKFK
#---------------------------------------------------------------
	
cmds.addAttr(globalLoc[0], ln = "Limb_Type", dataType = "string")
cmds.setAttr(globalLoc[0] + ".Limb_Type", "arm", type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "FK_ctl_01", dataType = "string")
cmds.setAttr(globalLoc[0] + ".FK_ctl_01", dadCtl, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "FK_ctl_02", dataType = "string")
cmds.setAttr(globalLoc[0] + ".FK_ctl_02", sonCtl, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "FK_ctl_03", dataType = "string")
cmds.setAttr(globalLoc[0] + ".FK_ctl_03", grandsonCtl, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "FK_poleVector", dataType = "string")
cmds.setAttr(globalLoc[0] + ".FK_poleVector", FKpvCtl, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "IK_ctl_01", dataType = "string")
cmds.setAttr(globalLoc[0] + ".IK_ctl_01", handIKctl, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "IK_poleVector", dataType = "string")
cmds.setAttr(globalLoc[0] + ".IK_poleVector", pvCtl, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "IK_jnt_01", dataType = "string")
cmds.setAttr(globalLoc[0] + ".IK_jnt_01", dadIK, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "IK_jnt_02", dataType = "string")
cmds.setAttr(globalLoc[0] + ".IK_jnt_02", sonIK, type = "string", lock=1)

cmds.addAttr(globalLoc[0], ln = "IK_jnt_03", dataType = "string")
cmds.setAttr(globalLoc[0] + ".IK_jnt_03", grandsonIK, type = "string", lock=1)