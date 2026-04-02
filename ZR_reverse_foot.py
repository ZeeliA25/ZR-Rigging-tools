#--------------------------------------------------------------#
#                     ZR Reverse Foot 		                   #
#                	  v.2025-08-14-001                		   #
#--------------------------------------------------------------#
import maya.cmds as cmds
from ZR_nameCon import*


#---------------------------------------------------------------
# Function : Reverse foot
#---------------------------------------------------------------

def ZR_reverseFoot(side, footCtl) :


	#create the set-up and place the locators 

	toeLoc = cmds.spaceLocator(name= ZR_nameCon(side, "toe", "locator" )) #placed on the toes sk
	toeEndLoc = cmds.spaceLocator(name= ZR_nameCon(side, "toeEnd", "locator" )) #placed on the toes se
	tipLoc = cmds.spaceLocator(name= ZR_nameCon(side, "tip", "locator" ))#placed on the toes se
	tiltOut = cmds.spaceLocator(name= ZR_nameCon(side, "tiltOut", "locator" ))
	tiltIn = cmds.spaceLocator(name= ZR_nameCon(side, "tiltIn", "locator" ))
	heelLoc = cmds.spaceLocator(name= ZR_nameCon(side, "heel", "locator" )) #placed on the ankle sk
	ballLoc = cmds.spaceLocator(name= ZR_nameCon(side, "ball", "locator" )) #placed on the toes sk
	ballEndLoc = cmds.spaceLocator(name= ZR_nameCon(side, "ballEnd", "locator" )) #placed on the ankle sk
	ballCenter = cmds.spaceLocator(name = ZR_nameCon(side, "ballCenter", "locator" )) #placed on the toes sk
	
	grp = cmds.group(em = True, n = ZR_nameCon( side, "reverseFoot", "group"))

	# placement and match transforms
	
	cmds.matchTransform(tiltIn, "locator1", pos = True, rot = False)
	cmds.matchTransform(tiltOut, "locator2", pos = True, rot = False)
	cmds.matchTransform(ballEndLoc, f"{side}_ankle_sk", pos = True, rot = False)
	cmds.matchTransform(heelLoc, f"{side}_ankle_se", pos = True, rot = False)
	cmds.matchTransform(toeLoc, f"{side}_toes_sk", pos = True, rot = False)
	cmds.matchTransform(toeEndLoc, f"{side}_toes_se", pos = True, rot = False)
	cmds.matchTransform(ballLoc, f"{side}_toes_sk", pos = True, rot = False)
	cmds.matchTransform(ballCenter, f"{side}_toes_sk", pos = True, rot = False)
	cmds.matchTransform(tipLoc, f"{side}_toes_se", pos = True, rot = False)
	
	cmds.matchTransform(grp, tiltOut)
	

	#hierarchy of the set-up

	cmds.parent(ballLoc, ballCenter)
	cmds.parent(ballEndLoc, ballLoc)
	cmds.parent(ballCenter, tipLoc)
	cmds.parent(toeLoc, tipLoc)
	cmds.parent(toeEndLoc, toeLoc)
	cmds.parent(tipLoc, heelLoc)
	cmds.parent(heelLoc, tiltIn)
	cmds.parent(tiltIn, tiltOut)
	cmds.parent(tiltOut, grp) 

	cmds.parent(grp, footCtl)


	# create the foot roll attributes

	cmds.addAttr(footCtl,k = True, ln="Reverse_Foot", at = "enum", en = "--------") 
	cmds.addAttr(footCtl,k = True, ln="Heel", at = "float", dv = 0, minValue = -5, maxValue = 5)
	cmds.addAttr(footCtl,k = True, ln="Tilt", at = "float", dv = 0, minValue = -5, maxValue = 5)
	cmds.addAttr(footCtl,k = True, ln="Ball", at = "float", dv = 0, minValue = 0, maxValue = 10)
	cmds.addAttr(footCtl,k = True, ln="Toes", at = "float", dv = 0, minValue = -5, maxValue = 5)
	cmds.addAttr(footCtl,k = True, ln="Tip", at = "float", dv = 0, minValue = -5, maxValue = 5)
	cmds.addAttr(footCtl,k = True, ln="Tip_Sides", at = "float", dv = 0, minValue = -5, maxValue = 5)

	
	# determine side for set driven keys values

	footName = footCtl.split("_")
	side = footName[0]

	if side == "L" :
		sideCoef = 1

	elif side == "R" :
		sideCoef = -1

	else :
		sideCoef = 1

	

	# Create the set driven keys

	cmds.setDrivenKeyframe(f"{heelLoc[0]}.rotateX", cd = f"{footCtl}.Heel")
	cmds.setAttr(f"{footCtl}.Heel", -5)
	cmds.setAttr(f"{heelLoc[0]}.rotateX", -60)
	cmds.setDrivenKeyframe(f"{heelLoc[0]}.rotateX", cd = f"{footCtl}.Heel")
	cmds.setAttr(f"{footCtl}.Heel", 5)
	cmds.setAttr(f"{heelLoc[0]}.rotateX", 35)
	cmds.setDrivenKeyframe(f"{heelLoc[0]}.rotateX", cd = f"{footCtl}.Heel")
	cmds.setAttr(f"{footCtl}.Heel", 0)

	cmds.setDrivenKeyframe(f"{tiltOut[0]}.rotateZ", cd = f"{footCtl}.Tilt")
	cmds.setAttr(f"{footCtl}.Tilt", -5)
	cmds.setAttr(f"{tiltOut[0]}.rotateZ", (-45*sideCoef) )
	cmds.setDrivenKeyframe(f"{tiltOut[0]}.rotateZ", cd = f"{footCtl}.Tilt")
	cmds.setAttr(f"{footCtl}.Tilt", 0)
	cmds.setDrivenKeyframe(f"{tiltIn[0]}.rotateZ", cd = f"{footCtl}.Tilt")
	cmds.setAttr(f"{footCtl}.Tilt", 5)
	cmds.setAttr(f"{tiltIn[0]}.rotateZ", (45*sideCoef) )
	cmds.setDrivenKeyframe(f"{tiltIn[0]}.rotateZ", cd = f"{footCtl}.Tilt")
	cmds.setAttr(f"{footCtl}.Tilt", 0)

	cmds.setDrivenKeyframe(f"{ballLoc[0]}.rotateX", cd = f"{footCtl}.Ball")
	cmds.setAttr(f"{footCtl}.Ball", 10)
	cmds.setAttr(f"{ballLoc[0]}.rotateX", 55 )
	cmds.setDrivenKeyframe(f"{ballLoc[0]}.rotateX", cd = f"{footCtl}.Ball")
	cmds.setAttr(f"{footCtl}.Ball", 0)

	cmds.setDrivenKeyframe(f"{toeLoc[0]}.rotateX", cd = f"{footCtl}.Toes")
	cmds.setAttr(f"{footCtl}.Toes", -5)
	cmds.setAttr(f"{toeLoc[0]}.rotateX", -25)
	cmds.setDrivenKeyframe(f"{toeLoc[0]}.rotateX", cd = f"{footCtl}.Toes")
	cmds.setAttr(f"{footCtl}.Toes", 5)
	cmds.setAttr(f"{toeLoc[0]}.rotateX", 35)
	cmds.setDrivenKeyframe(f"{toeLoc[0]}.rotateX", cd = f"{footCtl}.Toes")
	cmds.setAttr(f"{footCtl}.Toes", 0)

	cmds.setDrivenKeyframe(f"{tipLoc[0]}.rotateX", cd = f"{footCtl}.Tip")
	cmds.setAttr(f"{footCtl}.Tip", -5 )
	cmds.setAttr(f"{tipLoc[0]}.rotateX", -40)
	cmds.setDrivenKeyframe(f"{tipLoc[0]}.rotateX", cd = f"{footCtl}.Tip")
	cmds.setAttr(f"{footCtl}.Tip", 5 )
	cmds.setAttr(f"{tipLoc[0]}.rotateX", 75)
	cmds.setDrivenKeyframe(f"{tipLoc[0]}.rotateX", cd = f"{footCtl}.Tip")
	cmds.setAttr(f"{footCtl}.Tip", 0 )	

	cmds.setDrivenKeyframe(f"{tipLoc[0]}.rotateY", cd = f"{footCtl}.Tip_Sides")
	cmds.setAttr(f"{footCtl}.Tip_Sides", -5 )
	cmds.setAttr(f"{tipLoc[0]}.rotateY", (-45*sideCoef))
	cmds.setDrivenKeyframe(f"{tipLoc[0]}.rotateY", cd = f"{footCtl}.Tip_Sides")
	cmds.setAttr(f"{footCtl}.Tip_Sides", 5 )
	cmds.setAttr(f"{tipLoc[0]}.rotateY", (45*sideCoef))
	cmds.setDrivenKeyframe(f"{tipLoc[0]}.rotateY", cd = f"{footCtl}.Tip_Sides")
	cmds.setAttr(f"{footCtl}.Tip_Sides", 0 )
	
	return (toeEndLoc, ballLoc, ballEndLoc)


#---------------------------------------------------------------
# Function : Reverse foot on selection 
#---------------------------------------------------------------
def ZR_reverseFootSelection() :
	# define selection

	sel = cmds.ls(sl=True)
	footCtl = sel[0]
	selName = sel[0].split("_")
	print(selName[0])
	ZR_reverseFoot(selName[0], footCtl)
	
	