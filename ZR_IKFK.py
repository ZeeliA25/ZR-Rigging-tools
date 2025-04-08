#selctionner un joint pui sdeterminer les differentes parties du membre
#en fonction des entites on batit les nomenclatures chaines et controleurs
from nameCon import *
from ZR_makeControler import *
from ZR_displayCurve import *
from ZR_rotatePlane import *

#lister la selection 

sel = cmds.ls(sl=True, type = "joint")

#verifier qu' il n'y a qu'un joint de selectionne shoulder

if len(sel) != 1 :
	cmds.error("Too many arguments selected")

dad = sel[0]

#chercher les enfants et le parent de la selection
son = cmds.listRelatives(dad, c = True)

grandson = cmds.listRelatives(son, c = True)

grandDad = cmds.listRelatives(dad, p = True)

#chercher la position dans l'espace du membre (droite ou gauche ou centre)

spacePosition = cmds.xform(dad, query=1, t=1, ws=1 )
side = ""

if spacePosition[0] > 0 :
	side = "left"
elif spacePosition[0] < 0 :
	side = "right"
else :
	side = ""

dadSK = cmds.rename(dad, nameCon(side, "shoulder", "skin"))
sonSK = cmds.rename(son, nameCon(side, "elbow", "skin"))
grandsonSK = cmds.rename(grandson, nameCon(side, "wrist", "skin"))

#chercher la taille ? 

globalSize = cmds.getAttr("C_main_ctl" + ".GEO_SIZE")


#creation du global loc

globalLoc = cmds.spaceLocator(n = nameCon(side, "arm", "locator"))

#creation de l'attribut IKFK

IKFK = cmds.addAttr(globalLoc[0], k = True, ln="IKFK", defaultValue=1, minValue=0, maxValue=1, at = "float")
cmds.matchTransform(globalLoc[0], dadSK)
#chercher le groupe rigging s'il existe parenter le global dedans

if (cmds.objExists("RIGGING")) == 1 :
	cmds.parent(globalLoc[0], "RIGGING")

#la clavicule affecte le locator global

cmds.parentConstraint(grandDad[0], globalLoc, mo = 1)

###############FK system

#creation de controleur fk pour shoulder, elbow et wrist 
dadCtlBase = ZR_makeControler(dadSK)
sonCtlBase = ZR_makeControler(sonSK)
grandsonCtlBase = ZR_makeControler(grandsonSK)

dadCtl = cmds.rename(dadCtlBase[0], nameCon(side, "shoulder", "controller"))
sonCtl = cmds.rename(sonCtlBase[0], nameCon(side, "elbow", "controller"))
grandsonCtl = cmds.rename(grandsonCtlBase[0], nameCon(side, "wrist", "controller"))
dadGrp = cmds.rename(dadCtlBase[1], nameCon(side, "shoulder", "group"))
sonGrp = cmds.rename(sonCtlBase[1], nameCon(side, "elbow", "group"))
grandsonGrp = cmds.rename(grandsonCtlBase[1], nameCon(side, "wrist", "group"))

# Créer le PoleVector FK
FKpvBase = ZR_makeControler(sonSK)
FKpvCtl = cmds.rename(FKpvBase[0], nameCon(side, "FKarmPV", "controller"))
FKpvGrp = cmds.rename(FKpvBase[1], nameCon(side, "FKarmPV", "group"))

cmds.matchTransform(FKpvGrp, FKpvCtl)

#Placer le pole Vector

ZR_rotatePlane(dadSK, sonSK, grandsonSK)
cmds.matchTransform(FKpvGrp, "previz_loc")

#faire la hierarchie des controleurs 

cmds.parent(sonGrp, dadCtl)
cmds.parent(grandsonGrp, sonCtl)
cmds.parent(FKpvGrp, sonCtl)

#contrainte de la clavicule sur le groupe de placement du shoulder
cmds.parentConstraint(grandDad, dadGrp, mo=1)

#attribut follow sur le shoulder 
cmds.addAttr(dadCtl, k=1, ln="Follow", defaultValue=1, minValue=0, maxValue=1)

#blend de contrainte orient entre le monde et le chest

if (cmds.objExists("worldFollow_loc")) :
    worldLoc = "worldFollow_loc"
else :
    worldLoc = cmds.spaceLocator(n=nameCon("","worldFollow","locator"))
    cmds.parent(worldLoc, "RIGGING")
    
if (cmds.objExists("chestFollow_loc")) :
    chestLoc = "chestFollow_loc"
else :
    chestLoc = cmds.spaceLocator(n=nameCon("","chestFollow","locator"))
    cmds.parent(chestLoc, "RIGGING")
    
chest = cmds.listRelatives(grandDad, p = True)
cmds.matchTransform(chestLoc, chest, pos=True, rot=False)
offsetOrientFK = cmds.group(em = 1, name = nameCon(side, "offsetOrient", "group"))
cmds.matchTransform(offsetOrientFK, dadCtl)
cmds.parent(offsetOrientFK, dadGrp)
cmds.parent(dadCtl, offsetOrientFK)
followConstraint = cmds.orientConstraint(worldLoc, chestLoc, offsetOrientFK, mo=1)
reverseNode = cmds.createNode("reverse")
cmds.connectAttr(dadCtl + ".Follow", reverseNode + ".inputX")
cmds.connectAttr(reverseNode + ".outputX", followConstraint[0] + ".chestFollow_locW1.")
cmds.connectAttr(dadCtl + ".Follow", followConstraint[0] + ".worldFollow_locW0.") 


#proxy de l'attribut IKFK du controleur global sur les controleurs FK

cmds.addAttr(dadCtl, ln="IKFK", pxy= globalLoc[0] + ".IKFK")
cmds.addAttr(sonCtl, ln="IKFK", pxy= globalLoc[0] + ".IKFK")
cmds.addAttr(grandsonCtl, ln="IKFK", pxy= globalLoc[0] + ".IKFK")

#############IK system

#----------------------------------------------------------------
# IK System
#----------------------------------------------------------------
 
# Créer la chaîne de joints IK : dupliquer la chaine de skin, supprimer les doigts
 
IKchain = cmds.duplicate(dadSK, rc= 1 )

counter = 0
for IKjoint in IKchain :
	if counter < 3 :
		counter = counter+1
	else :
		if (objExists(IKjoint)) :
			cmds.delete(IKjoint)


# Renommer les joints IK
dadIK = cmds.rename(IKchain[0], nameCon(side, "shoulder", "rig"))
sonIK = cmds.rename(IKchain[1], nameCon(side, "elbow", "rig"))
grandsonIK = cmds.rename(IKchain[2], nameCon(side, "wrist", "rig"))
# Parenter la chaine IK au Locator Global
 
cmds.parent(dadIK, globalLoc[0])

# Créer le Controler IK de la main

handIKbase = ZR_makeControler(grandsonIK)
handIKctl = cmds.rename(handIKbase[0], nameCon(side, "hand", "controller"))
handIKgrp = cmds.rename(handIKbase[1], nameCon(side, "hand", "group"))

# Créer le PoleVector
pvBase = ZR_makeControler(sonIK)
pvCtl = cmds.rename(pvBase[0], nameCon(side, "armPV", "controller"))
pvGrp = cmds.rename(pvBase[1], nameCon(side, "armPV", "group"))

cmds.matchTransform(pvGrp, pvCtl)

#Placer le pole Vector
cmds.parent(pvGrp, sonIK)

cmds.matchTransform(pvGrp, "previz_loc")
cmds.delete("PREVIZ")

cmds.parent(pvGrp, "CONTROLLERS")

#Contrainte sur le pole Vector
mainCtl = "C_main_ctl"
cmds.addAttr(pvCtl, longName = "Follow_Main", attributeType = "float", k=1, min = 0, max=1, defaultValue=1)
pvParentConstraint = cmds.parentConstraint(mainCtl, handIKctl, pvGrp, mo=1)
cmds.setAttr(pvParentConstraint[0] + ".interpType", 2)

reverseNode = cmds.createNode("reverse")

cmds.connectAttr(pvCtl + ".Follow_Main", pvParentConstraint[0] + "." + mainCtl + "W0")
cmds.connectAttr(pvCtl + ".Follow_Main", reverseNode + ".inputX")
cmds.connectAttr(reverseNode + ".outputX", pvParentConstraint[0] + "." + handIKctl + "W1")

# Créer la curve d'affichage
curveIKPv = ZR_displayCurve(sonIK, pvCtl)
### Attribut "Follow World" sur le controler de la main IK
cmds.addAttr(handIKctl, ln = "Follow_World", k=1, defaultValue=1, minValue=0, maxValue=1)
### Blend de contrainte en le monde et la main IK
offsetOrientIK = cmds.group(em = 1, name = nameCon(side, "offsetOrientIK", "group"))
cmds.matchTransform(offsetOrientIK, handIKgrp)
cmds.parent(offsetOrientIK, handIKgrp)
cmds.parent(handIKctl, offsetOrientIK)
followIK = cmds.orientConstraint(worldLoc, offsetOrientIK, mo=1)
cmds.connectAttr(handIKctl + ".Follow_World", followIK[0] + ".worldFollow_locW0.")
# Renommer le controler IK et son groupe de placement
 
# Placement du PoleVector : dans un premier temps, placer sur le coude puis reculer sur Z
### UPDATE : Trouver le recul et le placement optimal du PoleVector
 
# Créer l'ikHandle et le parenter au controler, le cacher
ikRpHandle = cmds.ikHandle(n=nameCon(side, 'IKRP', 'handle') , startJoint=dadIK , endEffector=grandsonIK, solver="ikRPsolver")
cmds.parent(ikRpHandle[0], handIKctl)

cmds.setAttr(ikRpHandle[0]+".visibility", 0, lock=1)
cmds.setAttr(ikRpHandle[0]+".translate", lock=1)
cmds.setAttr(ikRpHandle[0]+".rotate", lock=1)
cmds.setAttr(ikRpHandle[0]+".scale", lock=1)
# Contraindre l'ikHandle par le Pole Vector
 
cmds.poleVectorConstraint(pvCtl, ikRpHandle[0])
 
# Contraindre en Orient le joint de main par le controler de la main IK

cmds.orientConstraint(handIKctl, grandsonIK)
 
### Stretch :)
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


#############Blend system

#parent constraint des controleurs aux joints

blendDad = cmds.parentConstraint(dadCtl, dadIK, dadSK)
cmds.setAttr(blendDad[0] + ".interpType", 2)

blendSon = cmds.parentConstraint(sonCtl, sonIK, sonSK)
cmds.setAttr(blendSon[0] + ".interpType", 2)

blendGrandson = cmds.parentConstraint(grandsonCtl, grandsonIK, grandsonSK)
cmds.setAttr(blendGrandson[0] + ".interpType", 2)



reverseNode = cmds.createNode("reverse")
cmds.connectAttr(globalLoc[0] +".IKFK", reverseNode +".inputX")
cmds.connectAttr(reverseNode +".outputX", blendDad[0] + "." + dadCtl + "W0")
cmds.connectAttr(globalLoc[0] +".IKFK", blendDad[0] + "." + dadIK + "W1")

cmds.connectAttr(reverseNode +".outputX", blendSon[0] + "." + sonCtl + "W0")
cmds.connectAttr(globalLoc[0] +".IKFK", blendSon[0] + "." + sonIK + "W1")

cmds.connectAttr(reverseNode +".outputX", blendGrandson[0] + "." + grandsonCtl + "W0")
cmds.connectAttr(globalLoc[0] +".IKFK", blendGrandson[0] + "." + grandsonIK + "W1")

cmds.connectAttr(globalLoc[0] + ".IKFK", handIKgrp + ".visibility")
cmds.connectAttr(globalLoc[0] + ".IKFK", curveIKPv + ".visibility")
cmds.connectAttr(globalLoc[0] + ".IKFK", pvGrp + ".visibility")

cmds.connectAttr(reverseNode + ".outputX", dadGrp + ".visibility")

ctrlList = cmds.ls(dadCtl, sonCtl, grandsonCtl, FKpvCtl, handIKctl, pvCtl, dadIK, sonIK, grandsonIK)

for ctrl in ctrlList :
    cmds.addAttr(ctrl, ln = "GLOBAL", dataType = "string")
    cmds.setAttr(ctrl + ".GLOBAL", globalLoc[0], type = "string", lock = 1)
	
	
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